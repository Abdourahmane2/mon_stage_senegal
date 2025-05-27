from anomalie_etudiant.detecter_anomalie_etudiant import detecter_anomalie_etudiant
from anomalie_personnel.detecter_anomalie_personnel import exporter_anomalies_personnel
# ============ Détecter toutes les anomalies ============

detecter_anomalie_etudiant(
    'C:/Users/HP/Desktop/mon_stage_senegal/data/Etudiants_2001_2024/Liste_globale_des_etudiants_tous_les_champs20012002.csv'
)

exporter_anomalies_personnel(
    'C:/Users/HP/Desktop/mon_stage_senegal/data/Personnel_2000_2024/Liste_agent_des_archive 2000.xlsx'
)
