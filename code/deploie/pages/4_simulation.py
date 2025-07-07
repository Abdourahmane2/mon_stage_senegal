import streamlit as st
st.set_page_config(page_title="Simulation d'Orientation UCAD", page_icon="🔍")
st.title("🤖 Lancer une simulation personnalisée pour visualiser vos options d'orientation.")
st.markdown("""
### 🎯 Évaluez vos chances de réussite en Licence 1 à l'UCAD

Dans cette page, vous choisissez un **département de formation** à l'UCAD, et l'IA analyse votre profil pour estimer vos **chances de redoubler** en première année.

Cette simulation repose sur les données réelles d'étudiants précédents et vous aide à mieux orienter votre choix.

🔍 **Trois niveaux de risque sont possibles** :
- 🔴 **Élevé** : forte probabilité de redoublement
- 🟠 **Moyen** : risque modéré
- 🟢 **Faible** : bonnes chances de réussite

> Cette estimation est indicative et ne remplace pas vos efforts personnels ni votre motivation.
""")
