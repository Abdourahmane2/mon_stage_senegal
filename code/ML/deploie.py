from io import BytesIO
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Orientation UCAD", layout="wide")

# --- Titre et introduction ---
st.title("🎓 Orientation UCAD : Où vont les étudiants comme vous ?")
st.markdown(""" Si vous décidez de venir a l'UCAD, vous aurez à choisir un département de formation en Licence 1. 
Cette application vous permet de **voir dans quels départements les étudiants comme vous ont été orientés l'année passé** et **quels sont les taux de réussite en L1 **.
""")

# --- Chargement et nettoyage des données ---
#https://drive.google.com/file/d/1pviwWW87UCyvs2_r9qYrHpxGZPrt-YGp/view?usp=sharing
@st.cache_data
@st.cache_data
def load_data():
    # API URL pour accéder à un fichier LFS
    url = "https://github.com/Abdourahmane2/donne_etudiant/raw/main/base_finale.csv"

    response = requests.get(url)
    if response.status_code != 200:
        st.error("❌ Échec du téléchargement.")
        st.stop()

    return pd.read_csv(BytesIO(response.content), low_memory=False)

try:
    data = load_data()
except Exception as e:
    st.error(f"❌ Erreur de chargement : {e}")

data = load_data()


data.columns = data.columns.str.lower().str.replace(" ", "_")
data['moyenne_annuelle'] = pd.to_numeric(data['moyenne_annuelle'], errors='coerce')

# Remplir les NaN par moyenne groupe
data['moyenne_annuelle'] = data.groupby(['resultat', 'mention_bacc'])['moyenne_annuelle'].transform(
    lambda x: x.fillna(x.mean())
)

# Classification du bac
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
    # Standardiser les mentions valides
    if mention == 'AB' or mention == 'Ab':
        return 'Assez Bien'
    elif mention == 'TB' or mention == 'TH':
        return 'Très Bien'
    elif mention == 'BI':
        return 'Bien'
    elif mention == 'A':
        return 'Assez Bien'
    elif mention == 'PA':
        return 'Passable'
    elif mention in ['KA', 'GU', 'MB', 'LO', '..', 'BA', 'LV', 'RU', 'HO' , '50']:
        return 'non renseigne'  


# Appliquer la fonction de nettoyage à la colonne 'mention_bacc'
data['mention_bacc'] = data['mention_bacc'].apply(clean_mention)

# Nettoyage des résultats
data['resultat'] = data['resultat'].map({
    'Redouble': 0, 'Passe': 1, 'Autorisé à passer': 1, 
    'A obtenu le diplôme': 1, 'Année validée': 1,
    'Exclu': 0, 'Année non validée': 0, 'Autorisé à faire la session 2': 1
})

# Nettoyage séries
import numpy as np
map_series = {
    'L1': 'L1', 'L1A': 'L1', 'L1B': 'L1', "L'1": 'L1', "L'": 'L1', 'L': 'L1',
    'L2': 'L2',
    'LA': 'LA',
    'ES': 'L1', 
    'A': 'L1', 'A2': 'L1', 'A3': 'L1', 'A4': 'L1',
    'B': 'L2',

    'S1': 'S1', 'S': 'S1', 'S1A': 'S1A',
    'S2': 'S2', 'S2A': 'S2A',
    'S3': 'S3',
    'S4': 'S4',
    'S5': 'S5',
    'C': 'S1',  
    'D': 'S2',  
    
    'T1': 'T1', 'T': 'T1',
    'T2': 'T2',

    'G': 'G', 'G2': 'G',
    'F6': 'F6',

    'SNB': 'S3', 'SNA': 'S5',
    'LAR': 'S5', 'SM': 'S5', 'STEG': 'S5',
    
    'E': None,
    np.nan: None
}

data['serie_bacc'] = data['serie_bacc'].astype(str).str.upper().str.strip()
data['serie_clean'] = data['serie_bacc'].map(map_series)

data['annee_bacc'] = pd.to_numeric(data['annee_bacc'], errors='coerce')
data = data[(data['annee_bacc'] >= 2020) & (data['annee_bacc'] <= 2100)]


#harmoniser la nationalité
data['nationalite'] = data['nationalite'].str.upper().str.strip()
print("Nationalités uniques :", data['nationalite'].unique())


# --- Interface utilisateur ---
st.sidebar.title("📋 Vos informations")
serie_bacc = st.sidebar.selectbox(" votre Série du Bac *", (data['serie_clean'].dropna().unique()))
annee_bacc = st.sidebar.selectbox(" votre année du Bac *", range(2021, 2025))
#nationnalite senegalaise par défaut
nationalite = st.sidebar.selectbox("Nationalité *", ['SÉNÉGALAISE'] + sorted(data['nationalite'].dropna().unique()))
mention_bacc = st.sidebar.selectbox("Mention que vous visez au bac (selon votre niveau)", ['Indifférent'] + sorted(data['mention_bacc'].dropna().unique()))
sexe = st.sidebar.selectbox("Votre sexe", data['sexe'].dropna().unique())



if st.sidebar.button("🔍 Voir les résultats"):
    if  not serie_bacc or not annee_bacc or not nationalite:
        st.error("Merci de remplir tous les champs obligatoires.")
        st.stop()
    # Filtrage
    filtered = data[
        (data['serie_clean'] == serie_bacc) &
        (data['annee_bacc'] == annee_bacc - 1) &
        (data['nationalite'].str.upper() == nationalite.upper())
        & (data['sexe'] == sexe)
    ]
    print(data['mention_bacc'].unique())
    print(data['serie_clean'].unique())
    print(data['annee_bacc'].unique())
    print(data['nationalite'].unique()) 

    if mention_bacc != 'Indifférent':
        filtered = filtered[filtered['mention_bacc'] == mention_bacc]

    nb_etudiants = len(filtered)
    if nb_etudiants == 0:
        st.warning("Aucun étudiant correspondant trouvé. Essayez d’élargir vos critères.")
        st.stop()

    st.success(f"🎉 {nb_etudiants} étudiant(s) similaires trouvés.")

    # Stats par département
    stats = []
    for dept in filtered['departement_formation'].unique():
        subset = filtered[filtered['departement_formation'] == dept]
        stats.append({
            "Département": dept,
            "Étudiants": len(subset),
            "Taux de réussite en L1 (%)": (subset['resultat'] == 1).mean() * 100,
            "taux_redoublement en L1 (%)": (subset['resultat'] == 0).mean() * 100 ,
            "Moyenne annuelle": subset['moyenne_annuelle'].mean()
        })
    stats_df = pd.DataFrame(stats).sort_values("Étudiants", ascending=False).head(5)

    # Affichage du tableau
    st.markdown("### 🏛️ Top 5 des départements où vont les étudiants comme vous")
    st.dataframe(stats_df, use_container_width=True)

    # Affichage du graphique
    st.markdown("### 📈 Taux de réussite dans ces départements")
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.barplot(data=stats_df, y="Département", x="Taux de réussite en L1 (%)", palette="Greens_d")
    ax.set_xlim(0, 100)
    st.pyplot(fig)

    # Recommandation
    #fonction pour prendre en entreer les nb etudiants et le taux de réussite
    def recommandation(stats_df):
        stats_df = stats_df.copy()
        
        # Normalisation sur 100
        stats_df['score_reussite'] = stats_df['Taux de réussite en L1 (%)']
        stats_df['score_taille'] = (stats_df['Étudiants'] / stats_df['Étudiants'].max()) * 100
        stats_df['score_moyenne'] = (stats_df['Moyenne annuelle'] / stats_df['Moyenne annuelle'].max()) * 100

        # Pondération
        stats_df['score_total'] = (
            0.5 * stats_df['score_reussite'] +
            0.3 * stats_df['score_taille'] +
            0.2 * stats_df['score_moyenne']
        )

        meilleur = stats_df.loc[stats_df['score_total'].idxmax()]
        return meilleur['Département']


   
    st.markdown("### ✅ Recommandation personnalisée")

    reco = recommandation(stats_df)

    st.success(f"""
    🎯 **D'après les parcours d'étudiants ayant un profil similaire au vôtre**, le département recommandé est :  
    ### 👉 `{reco}`

    Ce choix repose sur une combinaison de critères :
    - ✅ Un **bon taux de réussite** en première année (L1)
    - 👥 Une **forte présence d'étudiants** issus de la même série, nationalité et mention que vous
    - 📊 Une **stabilité des performances** observées sur les années précédentes

    ---

    💡 Cette recommandation est une **aide à la décision**, basée sur les données historiques d'orientation et de réussite à l'UCAD. Elle ne garantit pas votre réussite, mais vous donne une **indication pertinente**.

    🧭 **Pensez également à vos centres d'intérêt, votre motivation et vos ambitions professionnelles** pour faire un choix éclairé.
    """)


    st.warning("⚠️ Note : Ces données sont basées sur les parcours d'étudiants précédents orientes a l'UCAD. Elles ne garantissent pas votre réussite dans un département spécifique.")

    

else:
    st.info("Remplissez les champs à gauche et cliquez sur 'Voir les résultats'.") 
