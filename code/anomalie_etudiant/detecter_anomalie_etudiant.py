# %%
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# %%
data= pd.read_csv('C:/Users/HP/Desktop/mon_stage_senegal/data/Etudiants_2001_2024/Liste_globale_des_etudiants_tous_les_champs20012002.csv' , encoding='latin1' ,sep=';')


# %%
data.columns

# %%
#fonction  les  informations du dataframe
def afficher_info(df):
    df.info()
    print(f"il y'a {df.shape[0]} lignes et {df.shape[1]} colonnes.")



# %%
#======= Anomalie1 : les personnes avec un systeme lmd inscrit avant 2010 =========
def anomalie1(df):
    anomalie1_df = df[(df['ANNEE_INSCRIPTION'] < 2011) & (df['SYSTEME'] == 'LMD')]
    #afficher le niveau de formation

    if len(anomalie1_df) == 0:
        print("Il n'y a pas de personnes avec un système LMD inscrit avant 2011.(ceci n'est pas une anomalie !!!!!!)")
    else:
     print(f"il y'a {len(anomalie1_df)} personnes avec un systeme lmd inscrit inscrit avant 2011  .")
     niveau_formation = anomalie1_df['NIVEAU_SECTION'].unique()
     print(f"les niveaux de formation sont : {niveau_formation}")
    


# %%
#=========== Anomalie2 :  les valeurs manquantes dans les colonnes  ==========
from tabulate import tabulate
def anomalie2(df):
    valeurs_manquantes = df.isnull().sum()
    pourcentage_valeurs_manquantes = (valeurs_manquantes / len(df)) * 100

#tableau recapitulatif des valeurs manquantes
    tableau_valeurs_manquantes = pd.DataFrame({
        'Colonnes' : df.columns,
        'Valeurs manquantes': valeurs_manquantes,
        'Pourcentage': pourcentage_valeurs_manquantes
        }) .sort_values(by='Valeurs manquantes', ascending=False) 

    #les colonnes critiques avec plus de 50% de valeurs manquantes
    colonnes_critique = tableau_valeurs_manquantes[tableau_valeurs_manquantes['Pourcentage'] > 0]

    #visualisation des valeurs manquantes
    print("Tableau récapitulatif des valeurs manquantes :")
    print(tabulate(colonnes_critique, headers='keys', tablefmt='psql', showindex=False))
   

# %% [markdown]
# ici on vas reperer les année de naisance anormales 
# tous les personnes ayant passant le bac  avant  14 ans ou apres 40 ans sont consideres comme anormales 
# les personnes qui ont passes leur bac apres 30ans sont pas impossible mais tres rare 

# %%
#======anomalie3 :  les annéee de naissance pas bon ===============
from numpy import quantile

def anomalie3(data):
    # Convertir la colonne 'DATE_DE_NAISSANCE' en datetime
    data['DATE_DE_NAISSANCE'] = pd.to_datetime(data['DATE_DE_NAISSANCE'], errors='coerce')
    # Extraire l'année de naissance
    data['annee_naissance'] = data['DATE_DE_NAISSANCE'].dt.year
    print(data['annee_naissance'].unique())
    # Nettoyer et extraire uniquement les années de bac à 4 chiffres
    data['ANNEE_BACC'] = pd.to_numeric(
        data['ANNEE_BACC'].astype(str).str.extract(r'(\d{4})')[0], 
        errors='coerce'
    )
   # Calculer l'âge au bac uniquement pour les lignes valides
    data['age_bac'] = data['ANNEE_BACC'] - data['annee_naissance']
    print(data['age_bac']) 
    
   # Rechercher les personnes ayant passé le bac avant 14 ans
    personnes_bac_avant_14_ans = data[data['age_bac'] < 14]
    personnes_bac_apres_40ans = data[data['age_bac'] > 40]
    personnes_bac_apres_30ans = data[data['age_bac'] > 30]
    print(f"Il y a {personnes_bac_avant_14_ans.shape[0]} personnes qui ont passé le bac avant 14 ans. voici leur année de naissance et l'année de bac : \t")
    print(tabulate(personnes_bac_avant_14_ans[[ 'NUMERO' , 'DATE_DE_NAISSANCE', 'ANNEE_BACC' , 'age_bac']], headers='keys', tablefmt='psql', showindex=False))
    print(f"Il y a {personnes_bac_apres_40ans.shape[0]} personnes qui ont passé le bac avant 40 ans. voici leur année de naissance et l'année de bac : \t")
    print(tabulate(personnes_bac_apres_40ans[[ 'NUMERO' , 'DATE_DE_NAISSANCE', 'ANNEE_BACC' , 'age_bac']], headers='keys', tablefmt='psql', showindex=False))
    print(f"Il y a {personnes_bac_apres_30ans.shape[0]} personnes qui ont passé le bac avant 30 ans.! pas impossible mais rare")

    

# %% [markdown]
# on veut reperer les personnes qui font deux ou tois formations differentes 

# %%
def anomalie4(data):
    # Compter les doublons exacts (lignes identiques)
    total = data.duplicated(subset='NUMERO').sum()
    
    # Filtrer les étudiants apparaissant plusieurs fois avec le même numéro
    d = data[data.duplicated(subset=['NUMERO'], keep=False)]

    # Compter le nombre d'établissements différents pour chaque étudiant
    totale1 = d.groupby('NUMERO')['ETABLISSMENT_CODE'].nunique()

    # Compter combien d'étudiants ont étudié dans plusieurs établissements
    nb_personnes_2_formations = (totale1 == 2).sum()
    nb_personnes_3_formations = (totale1 == 3).sum()
    nb_personnes_4_formations = (totale1 == 4).sum()
    nb_personnes_plus_4 = (totale1 > 4).sum()

    print(f"Il y a {total} doublons exacts dans le DataFrame.")
    print(f"Il y a {nb_personnes_2_formations} personnes qui ont étudié dans 2 établissements différents.")
    print(f"Il y a {nb_personnes_3_formations} personnes qui ont étudié dans 3 établissements différents.")
    print(f"Il y a {nb_personnes_4_formations} personnes qui ont étudié dans 4 établissements différents.")
    print(f"Il y a {nb_personnes_plus_4} personnes qui ont étudié dans plus de 4 établissements différents.")
    
    
  


# %%
#afficher les mentions de bac valides 
data['MENTION_BACC'].unique()

# %% [markdown]
# on remarque des mentions de bac pas normales comme '50' , '15' etc........

# %%
#========== anomalie5 : les mentions au bac pas normales  ===========
def anomalie5(data):
    #les mentions au bac pas normales
    compteur = 0 
    mentions_normales  = ['AB', 'B', 'TB', 'PA']
    #compter le nombre de mentions anormales
    for i in data['MENTION_BACC']:
        if i not in mentions_normales:
            compteur+=1 
        
    print(f"il y'a {compteur} mentions anormales au bac")
    #afficher les mentions anormales
    mentions_anormales = data[~data['MENTION_BACC'].isin(mentions_normales)]['MENTION_BACC'].unique()
    print("les mentions anormales sont : ", mentions_anormales)
 

# %% [markdown]
# les personnes qui ont basse apres le bac apartir de 1998 auront comme serie de bac [L1B,S1A,S1,L1A,S3,S4,T1,STEG,SEA,F6,S5,S2,STIDD,LA,T2,L-AR,L2,L'1]
# les personnes qui ont passe le bac avant 1998 auront comme seri series_bac_avant_1998 = ["A1", "A2", "A3", "A4", "C", "D", "E",  "F1", "F2", "F3", "F4" ,"F5", "F6", "F7",  "G1", "G2", "G3",  "T1", "T2",  "L'", "S'"  ]

# %%
data['SERIE_BACC'].unique()

# %%
#==========anomalie6 : les series de bac pas valides =======
def anomalie6(data):
    #les series de bac pas valides
    compteur = 0 
    compteur1 = 0
    series_normales_avant_98 = [ "A1", "A2", "A3", "A4",  "C", "D", "E","F1", "F2", "F3", "F4", "F5", "F6", "F7", "G1", "G2", "G3",  "T1", "T2",  "L'", "S'"  ]  
    series_normales_apres_98 = ["L1B", "S1A", "S1", "L1A", "S3", "S4", "T1", "STEG", "SEA", "F6","S5", "S2", "STIDD", "LA", "T2", "L-AR", "L2", "L'1"]         
     #convertir la colonne 'ANNEE_BACC' en entier
    data['ANNEE_BACC'] = pd.to_numeric(data['ANNEE_BACC'], errors='coerce')
    #compter le nombre de series anormales
    for _, i in data.iterrows():
        if i['SERIE_BACC'] not in series_normales_avant_98 and i['ANNEE_BACC'] < 1998:
            compteur+=1 
        if i['SERIE_BACC'] not in series_normales_apres_98 and i['ANNEE_BACC'] >= 1998:
            compteur1+=1    
        
    print(f"il y'a {compteur} qui ont passe leur bac avant  1998 qui une serie de bac pas normale")
    #afficher les series anormales
    series_anormales = data[~data['SERIE_BACC'].isin(series_normales_avant_98) & (data['ANNEE_BACC'] < 1998)]['SERIE_BACC'].unique()
    print("ces series sont : ", series_anormales)
    print(f"il y'a {compteur1} qui ont passe leur bac apres  1998 qui une serie de bac pas normale")
    #afficher les series anormales
    series_anormales1 = data[~data['SERIE_BACC'].isin(series_normales_apres_98) & (data['ANNEE_BACC'] >= 1998)]['SERIE_BACC'].unique()
    print("ces series sont : ", series_anormales1)
    
     
  

# %%
#==========anomalie6 : les series de bac pas valides =======
def anomalie6(data):
    #les series de bac pas valides  
    compteur = 0 
    compteur1 = 0
    series_normales_avant_98 = [ "A1", "A2", "A3", "A4",  "C", "D", "E","F1", "F2", "F3", "F4", "F5", "F6", "F7", "G1", "G2", "G3",  "T1", "T2",  "L'", "S'"  ]  
    series_normales_apres_98 = ["L1B", "S1A", "S1", "L1A", "S3", "S4", "T1", "STEG", "SEA", "F6","S5", "S2", "STIDD", "LA", "T2", "L-AR", "L2", "L'1"]         
     #convertir la colonne 'ANNEE_BACC' en entier
    data['ANNEE_BACC'] = pd.to_numeric(data['ANNEE_BACC'], errors='coerce')
    #compter le nombre de series anormales
    for _, i in data.iterrows():
        if i['SERIE_BACC'] not in series_normales_avant_98 and i['ANNEE_BACC'] < 1998:
            compteur+=1 
        if i['SERIE_BACC'] not in series_normales_apres_98 and i['ANNEE_BACC'] >= 1998:
            compteur1+=1    
        
    print(f"il y'a {compteur} qui ont passe leur bac avant  1998 qui une serie de bac pas normale")
    #afficher les series anormales
    series_anormales = data[~data['SERIE_BACC'].isin(series_normales_avant_98) & (data['ANNEE_BACC'] < 1998)]['SERIE_BACC'].unique()
    print("ces series sont : ", series_anormales)
    print(f"il y'a {compteur1} qui ont passe leur bac apres  1998 qui une serie de bac pas normale")
    #afficher les series anormales
    series_anormales1 = data[~data['SERIE_BACC'].isin(series_normales_apres_98) & (data['ANNEE_BACC'] >= 1998)]['SERIE_BACC'].unique()
    print("ces series sont : ", series_anormales1)
    
     
  

# %%
#================= afficher toutes les anomalies ===================

# %%
import os
import os
import io
import contextlib
import pandas as pd

def detecter_anomalie_etudiant(fichier_entree ):
    # Lire le fichier (Excel ou CSV automatiquement détecté)
    extension = os.path.splitext(fichier_entree)[1].lower()
    if extension == '.csv':
        data = pd.read_csv(fichier_entree , encoding='latin1', sep=';')
    elif extension in ['.xls', '.xlsx']:
        data = pd.read_excel(fichier_entree)
    else:
        raise ValueError("Format de fichier non supporté. Utilisez .csv, .xls ou .xlsx")

    # Construire le nom du fichier de sortie
    nom_base = os.path.splitext(os.path.basename(fichier_entree))[0]
    nom_sortie = f"anomalies_{nom_base}.txt"

    # Liste des fonctions d'anomalies
    fonctions_anomalies = [ afficher_info ,  anomalie1, anomalie2, anomalie3, anomalie4, anomalie5 , anomalie6]

    # Rediriger la sortie print vers un fichier texte
    with open(nom_sortie, 'w', encoding='utf-8') as f:
        f.write(f"===== liste des anomalies pour le fichier  {fichier_entree} =====\n\n")
        for i, fonction in enumerate(fonctions_anomalies, 1):
            f.write(f"===== Anomalie {i} =====\n")
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                fonction(data)
            f.write(buffer.getvalue())
            f.write("\n\n")
            
    print(f"Les anomalies ont été détectées et enregistrées dans le fichier : {nom_sortie}")
    



