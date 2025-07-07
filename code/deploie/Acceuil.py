
import os
import streamlit as st

st.set_page_config(page_title="Orientation UCAD", layout="wide") 


st.title("🎓 Orientation UCAD : Où vont les étudiants comme vous ?")

pages = [f.replace(".py", "") for f in os.listdir("pages") if f.endswith(".py")]

# Affichage avec noms en majuscules
choix = st.sidebar.selectbox("Navigation", [page.upper() for page in pages])

st.markdown("""
Bienvenue sur l'outil d'aide  aux choix pour les élèves désirant s'inscrire à l'UCAD via Campusen !

Ce service vous accompagne dans votre choix de département en Licence 1 selon votre profil et vos envies.

---

### Que pouvez-vous faire ici ?

-  **Explorer les départements les plus choisis** par les étudiants selon leurs profils.
-  **Participer à un quiz d'orientation** pour mieux cerner vos intérêts et aptitudes.
-  **Lancer une simulation personnalisée** pour visualiser vos options d'orientation.
-  **Voir les débouchés possibles** pour chaque département.

---

Pour commencer, utilisez la barre latérale à gauche pour naviguer entre les différentes fonctionnalités.

Bonne découverte et bon courage dans votre parcours ! 
""")
