import streamlit as st

st.set_page_config(page_title="Quiz d'orientation UCAD")
st.title("**Quiz d'orientation** pour mieux cerner vos intérêts et aptitudes")

st.markdown("""
Bienvenue dans le quiz d'orientation de l'Université Cheikh Anta Diop (UCAD) !  
Ce quiz est conçu pour vous aider à mieux comprendre vos intérêts, vos aptitudes et vos préférences académiques.  
Répondez honnêtement aux questions pour obtenir une suggestion de département qui vous correspond.
""")

# ───── Questionnaire ─────
st.subheader("🔍 **Questionnaire**")

questions = [
    "1. Quelle est ta série actuelle ?",
    "2. Quelle est ta matière préférée ?",
    "3. Quel type d'activité préfères-tu ?",
    "4. Quel environnement de travail t'attire le plus ?"
]

options = [
    ["Scientifique", "Littéraire", "Technique", "Gestion"],
    ["Mathématiques", "Physique / Chimie", "SVT / Biologie", "Français / Philosophie", "Histoire / Géographie", "Langues étrangères", "Sciences économiques et sociales", "Informatique / Technologie"],
    ["Aider ou écouter les autres", "Résoudre des énigmes, faire des calculs", "Lire, écrire, débattre", "Créer (dessin, musique, photo…)", "Travailler avec mes mains", "Voyager, découvrir d'autres cultures"],
    ["Un hôpital ou une clinique", "Un laboratoire ou un bureau d'études", "Un studio artistique ou une scène", "Une entreprise, un bureau", "Une salle de classe"]
]

responses = []

# Collecte des réponses
for i, question in enumerate(questions):
    response = st.selectbox(
        question,
        options[i],
        key=i,
        help=f"Choisissez une réponse pour la question {i + 1}.",
        placeholder="Sélectionnez une réponse"
    )
    responses.append(response)

# ───── Résultat ─────
if st.button("Valider les réponses"):
    st.success("Vos réponses ont été enregistrées ! 🎉")

    st.subheader(" **Vos réponses**")
    for i, response in enumerate(responses):
        st.write(f"{questions[i]}  {response}")

    # ───── Suggestions de département ─────
    st.subheader(" **Département suggéré**")

    suggestion = ""

    if responses[0] == "Scientifique":
        if responses[1] in ["Mathématiques", "Physique / Chimie"] and responses[2] == "Résoudre des énigmes, faire des calculs":
            suggestion = " **Informatique, Génie logiciel, Data Science**"
        elif responses[1] == "SVT / Biologie" and responses[3] == "Un hôpital ou une clinique":
            suggestion = " **Médecine, Sciences de la santé**"
        elif responses[2] == "Travailler avec mes mains":
            suggestion = " **Génie mécanique, Électrotechnique**"
        else:
            suggestion = " **Sciences fondamentales ou ingénierie**"

    elif responses[0] == "Littéraire":
        if responses[2] == "Lire, écrire, débattre":
            suggestion = " **Lettres, Journalisme, Communication**"
        elif responses[2] == "Créer (dessin, musique, photo…)":
            suggestion = " **Arts, Design graphique, Audiovisuel**"
        else:
            suggestion = " **Langues, Histoire ou Philosophie**"

    elif responses[0] == "Technique":
        if responses[1] == "Informatique / Technologie":
            if responses[2] == "Travailler avec mes mains":
                suggestion = " **Réseaux, Électronique, Robotique**"
            elif responses[2] == "Résoudre des énigmes, faire des calculs":
                suggestion = " **Développement web, Cybersécurité**"
            else:
                suggestion = " **Technologie industrielle, maintenance**"
        else:
            suggestion = " **Formation technique spécialisée**"

    elif responses[0] == "Gestion":
        if responses[2] == "Voyager, découvrir d'autres cultures":
            suggestion = " **Commerce international, Marketing**"
        else:
            suggestion = " **Comptabilité, Gestion, Management**"

    else:
        suggestion = " **Aucune correspondance exacte. Veuillez affiner vos réponses.**"

    # Affichage du département final
    st.success(f"Nous vous suggérons : {suggestion}")
