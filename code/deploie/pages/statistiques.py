from io import BytesIO
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time


with st.spinner("⏳ Cette page peut prendre un peu de temps à charger car nous téléchargeons une grande base de donnée. Veuillez patienter..." ):
    time.sleep(3) # À remplacer par ton vrai traitemen
st.title("📊 Statistiques d'Orientation UCAD") 
st.markdown("""
Si vous décidez de venir à l'UCAD, vous aurez à choisir un département de formation en Licence 1. 
Cette application vous permet de **voir dans quels départements les étudiants comme vous ont été orientés l'année passée** et **quels sont les taux de réussite en L1**.
""")


@st.cache_data
def load_and_clean_data():
    url = "https://github.com/Abdourahmane2/donne_etudiant/raw/main/base_finale.csv"
    response = requests.get(url)
    if response.status_code != 200:
        st.error("❌ Échec du téléchargement.")
        st.stop()

    data = pd.read_csv(BytesIO(response.content), low_memory=False)

    data.columns = data.columns.str.lower().str.replace(" ", "_")
    data['moyenne_annuelle'] = pd.to_numeric(data['moyenne_annuelle'], errors='coerce')
    data['moyenne_annuelle'] = data.groupby(['resultat', 'mention_bacc'])['moyenne_annuelle'].transform(lambda x: x.fillna(x.mean()))

    def serie_bac_type(serie):
        s = str(serie).upper().strip()
        if any(x in s for x in ['S', 'SCI', 'D', 'E', 'F6', 'F4', 'F5', 'S2', 'S3']):
            return 'Scientifique'
        elif any(x in s for x in ['L', 'A', 'AR']):
            return 'Littéraire'
        elif any(x in s for x in ['G', 'T', 'STG']):
            return 'Tertiaire'
        return 'Autre'

    data['categorie_bac'] = data['serie_bacc'].apply(serie_bac_type)

    def clean_mention(mention):
        mention = str(mention).upper().strip()
        if mention in ['AB', 'A']: return 'Assez Bien'
        if mention in ['TB', 'TH']: return 'Très Bien'
        if mention == 'BI': return 'Bien'
        if mention == 'PA': return 'Passable'
        if mention in ['KA', 'GU', 'MB', 'LO', '..', 'BA', 'LV', 'RU', 'HO', '50']:
            return 'non renseigne'
        return mention

    data['mention_bacc'] = data['mention_bacc'].apply(clean_mention)

    data['resultat'] = data['resultat'].map({
        'Redouble': 0, 'Passe': 1, 'Autorisé à passer': 1, 
        'A obtenu le diplôme': 1, 'Année validée': 1,
        'Exclu': 0, 'Année non validée': 0, 'Autorisé à faire la session 2': 1
    })

    map_series = {
        'L1': 'L1', 'L1A': 'L1', 'L1B': 'L1', "L'1": 'L1', "L'": 'L1', 'L': 'L1',
        'L2': 'L2', 'LA': 'LA', 'ES': 'L1', 'A': 'L1', 'A2': 'L1', 'A3': 'L1', 'A4': 'L1',
        'B': 'L2', 'S1': 'S1', 'S': 'S1', 'S1A': 'S1A', 'S2': 'S2', 'S2A': 'S2A',
        'S3': 'S3', 'S4': 'S4', 'S5': 'S5', 'C': 'S1', 'D': 'S2', 'T1': 'T1', 'T': 'T1',
        'T2': 'T2', 'G': 'G', 'G2': 'G', 'F6': 'F6', 'SNB': 'S3', 'SNA': 'S5',
        'LAR': 'S5', 'SM': 'S5', 'STEG': 'S5', 'E': None, np.nan: None
    }

    data['serie_bacc'] = data['serie_bacc'].astype(str).str.upper().str.strip()
    data['serie_clean'] = data['serie_bacc'].map(map_series)

    data['annee_bacc'] = pd.to_numeric(data['annee_bacc'], errors='coerce')
    data = data[(data['annee_bacc'] >= 2020) & (data['annee_bacc'] <= 2100)]

    data['nationalite'] = data['nationalite'].str.upper().str.strip()

    return data

data = load_and_clean_data()

st.sidebar.title("\U0001F4CB Vos informations")
serie_bacc = st.sidebar.selectbox("Votre Série du Bac *", sorted(data['serie_clean'].dropna().unique()))
annee_bacc = st.sidebar.selectbox("Votre année du Bac *", range(2021, 2025))
nationalite = st.sidebar.selectbox("Nationalité *", ['SÉNÉGALAISE'] + sorted(data['nationalite'].dropna().unique()))
mention_bacc = st.sidebar.selectbox("Mention que vous visez au bac selon votre niveau", ['Indifférent'] + sorted(data['mention_bacc'].dropna().unique()))
sexe = st.sidebar.selectbox("Votre sexe", data['sexe'].dropna().unique())

if st.sidebar.button("\U0001F50D Voir les résultats"):
    filtered = data[
        (data['serie_clean'] == serie_bacc) &
        (data['annee_bacc'] == annee_bacc - 1) &
        (data['nationalite'].str.upper() == nationalite.upper()) &
        (data['sexe'] == sexe)
    ]

    if mention_bacc != 'Indifférent':
        filtered = filtered[filtered['mention_bacc'] == mention_bacc]

    nb_etudiants = len(filtered)
    if nb_etudiants == 0:
        st.warning("Aucun étudiant correspondant trouvé. Essayez d’élargir vos critères.")
        st.stop()

    st.success(f"\U0001F389 {nb_etudiants} étudiant(s) similaires trouvés.")

    stats = []
    for dept in filtered['departement_formation'].dropna().unique():
        subset = filtered[filtered['departement_formation'] == dept]
        stats.append({
            "Département": dept,
            "Étudiants": len(subset),
            "Taux de réussite en L1 (%)": (subset['resultat'] == 1).mean() * 100,
            "taux_redoublement en L1 (%)": (subset['resultat'] == 0).mean() * 100,
            "Moyenne annuelle": subset['moyenne_annuelle'].mean()
        })
    stats_df = pd.DataFrame(stats).sort_values("Étudiants", ascending=False).head(5)

    st.markdown("### \U0001F3DB️ Top 5 des départements où vont les étudiants comme vous")
    st.dataframe(stats_df, use_container_width=True)

    st.markdown("### \U0001F4C8 Taux de réussite dans ces départements")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=stats_df, y="Département", x="Taux de réussite en L1 (%)", palette="Greens_d")
    ax.set_xlim(0, 100)
    st.pyplot(fig)

    def recommandation(stats_df):
        stats_df = stats_df.copy()
        stats_df['score_reussite'] = stats_df['Taux de réussite en L1 (%)']
        stats_df['score_taille'] = (stats_df['Étudiants'] / stats_df['Étudiants'].max()) * 100
        stats_df['score_moyenne'] = (stats_df['Moyenne annuelle'] / stats_df['Moyenne annuelle'].max()) * 100
        stats_df['score_total'] = 0.5 * stats_df['score_reussite'] + 0.3 * stats_df['score_taille'] + 0.2 * stats_df['score_moyenne']
        meilleur = stats_df.loc[stats_df['score_total'].idxmax()]
        return meilleur['Département']

    reco = recommandation(stats_df)
    #afficher lui des debouches potentiels

    st.markdown("### ✅ Recommandation personnalisée")
    st.success(f"""
    \U0001F3AF **D'après les parcours d'étudiants ayant un profil similaire au vôtre**, le département recommandé est :  
    ### 👉 `{reco}` 

    Ce choix repose sur une combinaison de critères :
    - ✅ Un **bon taux de réussite** en première année (L1)
    - 👥 Une **forte présence d'étudiants** issus de la même série, nationalité et mention que vous
    - \U0001F4CA Une **stabilité des performances** observées sur les années précédentes
    - ℹ️ Pour mieux choisir, **n'oubliez pas de consulter les débouchés liés à ce département**.
        Cela peut vous aider à mieux comprendre les métiers accessibles et à projeter votre avenir professionnel.
""")

    st.warning("⚠️ Note : Ces données sont basées sur les parcours d'étudiants précédents orientés à l'UCAD. Elles ne garantissent pas votre réussite dans un département spécifique.")


else:
    st.info("Remplissez les champs à gauche et cliquez sur 'Voir les résultats'.")
