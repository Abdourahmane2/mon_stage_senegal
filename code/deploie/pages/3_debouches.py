import streamlit as st

st.set_page_config(page_title="Débouchés", page_icon="💼", layout="wide")

st.title("💼 Débouchés des départements de formation à l'UCAD")

st.markdown("""
### 🎓 Explorez les débouchés professionnels pour chaque département de formation à l'UCAD.
Sélectionnez une faculté ci-dessous pour découvrir les possibilités.
""")

# Dictionnaire des départements et débouchés
departements = {
    "FSJP": {
        "Histoire du droit": [
            "Enseignant-chercheur en histoire du droit",
            "Archiviste ou conservateur du patrimoine juridique",
            "Juriste spécialisé en droit ancien"
        ],
        "Droit public": [
            "Administrateur territorial",
            "Juriste en collectivité locale ou dans une institution publique",
            "Chargé des affaires juridiques dans les ONG ou ministères"
        ],
        "Droit privé": [
            "Avocat en droit civil ou des affaires",
            "Juriste d'entreprise",
            "Notaire ou clerc de notaire"
        ],
        "Science politique": [
            "Analyste politique ou géopolitique",
            "Chargé de mission dans une organisation internationale",
            "Conseiller en communication politique"
        ]
    },

   "FST": {
    "Département de Mathématiques-Informatique": [
        "Développeur web / mobile",
        "Data Scientist",
        "Ingénieur en intelligence artificielle",
        "Administrateur systèmes et réseaux",
        "Chercheur en informatique théorique"
    ],
    "Département de Chimie": [
        "Chimiste dans l'industrie pharmaceutique ou cosmétique",
        "Ingénieur chimiste en formulation ou qualité",
        "Chercheur en chimie organique ou analytique",
        "Technicien en laboratoire de contrôle",
        "Enseignant-chercheur"
    ],
    "Département de Biologie Animale": [
        "Zoologiste ou écologue",
        "Chargé d'études en biodiversité animale",
        "Technicien en biologie animale ou vétérinaire",
        "Chercheur en biologie cellulaire ou physiologie animale",
        "Spécialiste en conservation de la faune"
    ],
    "Département de Biologie Végétale": [
        "Botaniste ou phytopathologiste",
        "Chargé d'études en environnement ou reboisement",
        "Chercheur en biotechnologies végétales",
        "Agronome spécialisé",
        "Technicien en laboratoire végétal"
    ],
    "Département de Géologie": [
        "Géologue minier ou pétrolier",
        "Hydrogéologue",
        "Géotechnicien en BTP",
        "Cartographe / analyste SIG",
        "Chercheur en sciences de la Terre"
    ],
    "Département de Physique": [
        "Ingénieur en instrumentation ou électronique",
        "Chercheur en physique appliquée ou fondamentale",
        "Technicien en laboratoire de mesure",
        "Spécialiste en énergies renouvelables",
        "Enseignant-chercheur en physique"
    ]
} ,
 
  "FLSH": { 
    "Institut des Langues Étrangères Appliquées (ILEA)": [
        "Traducteur / Interprète professionnel",
        "Chargé de communication internationale",
        "Assistant multilingue dans les entreprises ou ONG",
        "Responsable export ou commercial à l'international"
    ],
    "Département de Philosophie": [
        "Enseignant-chercheur en philosophie",
        "Conseiller en éthique ou communication",
        "Chargé de mission dans les institutions culturelles",
        "Rédacteur ou journaliste spécialisé"
    ],
    "Département d'Allemand": [ 
        "Professeur d'allemand",
        "Traducteur ou interprète",
        "Attaché linguistique dans les ambassades ou organismes internationaux"
    ],
    "Département d'Arabe classique": [ 
        "Professeur d'arabe",
        "Traducteur littéraire ou juridique",
        "Expert en culture et civilisation arabo-islamique"
    ],
    "Département d'Histoire": [
        "Archiviste / Documentaliste",
        "Chercheur ou enseignant-chercheur",
        "Chargé de mission dans les musées ou institutions patrimoniales",
        "Guide conférencier / Médiateur culturel"
    ],
    "Département de Langues Romanes (espagnol, italien, portugais)": [
        "Professeur de langues romanes",
        "Traducteur ou interprète",
        "Chargé de coopération internationale",
        "Attaché culturel ou médiateur linguistique"
    ], 
    "Département d'Anglais": [
        "Professeur d'anglais",
        "Traducteur / Interprète",
        "Chargé de relations internationales",
        "Rédacteur en communication anglophone"
    ], 
    "Département de Géographie": [ 
        "Urbaniste / Aménageur du territoire",
        "Cartographe / Spécialiste SIG",
        "Chargé d'études environnementales",
        "Enseignant ou chercheur en géographie"
    ], 
    "Département de Sociologie": [
        "Sociologue ou chercheur en sciences sociales",
        "Chargé d'études dans les ONG ou collectivités",
        "Conseiller en politiques publiques ou développement local",
        "Enquêteur ou analyste social"
    ]
} , 
"FMPOS": {
    "Département de Chirurgie et Spécialités Chirurgicales": [
        "Chirurgien général",
        "Chirurgien orthopédiste ou urologue",
        "Spécialiste en ORL ou ophtalmologie"
    ],
    "Département de Médecine et Spécialités Médicales": [
        "Médecin généraliste ou spécialiste (cardiologue, pneumologue, etc.)",
        "Médecin hospitalier ou libéral",
        "Médecin en santé publique"
    ],
    "Biologie Médicale et d'Explorations Fonctionnelles": [
        "Biologiste médical en laboratoire",
        "Spécialiste en analyses biomédicales",
        "Responsable de laboratoire d'analyses"
    ],
    "Sciences Biologiques et Pharmaceutiques Appliquées": [
        "Pharmacologue ou toxicologue",
        "Chercheur en biotechnologies ou pharmacologie",
        "Responsable contrôle qualité dans l'industrie pharmaceutique"
    ],
    "Sciences Pharmaceutiques, Physiques et Chimiques": [
        "Pharmacien galéniste ou analyste",
        "Responsable de production en industrie pharmaceutique",
        "Pharmacien hospitalier ou officinal"
    ],
    "Département d'Odontologie (IOS)": [
        "Chirurgien-dentiste",
        "Orthodontiste",
        "Spécialiste en implantologie ou dentisterie esthétique"
    ]
}

}
liens_facultes = {
            "FSJP": "https://www.ucad.sn/fsjp",
            "FST": "https://www.ucad.sn/fst",
            "FLSH": "https://www.ucad.sn/flsh",
            "FMPOS": "https://www.ucad.sn/fmpos"
        }

# Création des onglets par faculté
facultes = list(departements.keys())
tabs = st.tabs(facultes)

for i, faculte in enumerate(facultes):
    with tabs[i]:
        st.header(f"🏛️ Faculté : {faculte}")
        st.markdown("Cliquez sur un département pour voir ses débouchés.")
        for nom_dept, debouches in departements[faculte].items():
            with st.expander(f"📘 {nom_dept}"):
                st.markdown("**Débouchés :**")
                for metier in debouches:
                    st.markdown(f"- {metier}")
        if faculte in liens_facultes:
            st.markdown(f"👉 [En savoir plus sur le site officiel de la {faculte}]({liens_facultes[faculte]})", unsafe_allow_html=True)                


st.markdown("### 📌 Remarque importante")

st.warning(""" ces liste ne représente pas l'intégralité des débouchés possibles.
Consultez les sites officiels des facultés pour plus d'informations.""")