# %% [markdown]
# detecter les anomalies liees aux données du personnel de maniere globale 
# - PER : personnel Enseignat 
# - PATS : Personnel administratif

# %%
import pandas as pd 
import numpy as np 

# %% [markdown]
# lire les données

# %%
data = pd.read_excel('C:/Users/HP/Desktop/mon_stage_senegal/data/Personnel_2000_2024/Liste_agent_des_archive 2000.xlsx') 

# %%


# %%


# %%


# %% [markdown]
# le fichier contient 91 colonnes et 1587 lignes 

# %% [markdown]
# #### anomalie1 : des personnes recrutes apres leur prise de services c'est a dire date_recrutement > data_prise de service 

# %%
def anomalie_recrutement(df):
    anomalie1_df = df[df['DATE RECRUTEMENT'] > (df['DATE PRISE SERVICE'])]
    if len(anomalie1_df) == 0:
        print("tous les agents ont une date de recrutement valide.")
    else:
     print(f"# {len(anomalie1_df)} agents ont une anomalie de date de recrutement. leur date de recrutement est supérieure à leur date de prise de service.")
  
    

# %% [markdown]
# solution possible : supprimer ces lignes car leur faible nombre (5/1587) les rend negligeables 

# %% [markdown]
# #### anomalie2 : des personnes retraites avant d'etre recrutes c'est a dire date retraite < date recrutement 

# %%
def anomalie_retraite(df):
    anomalie1_df = df[df['DATE RETRAITE'] < (df['DATE RECRUTEMENT'])]
    if len(anomalie1_df) == 0:
        print("tous les agents ont une date de retraite valide (ceci n'est pas une anomalie !!!)")
    else:
     print(f"# {len(anomalie1_df)} agents ont une anomalie de date de retraite. leur date de retraite est inferieur à leur date de prise de recrutement.")
     


# %% [markdown]
# #### anomalie3 : fin de poste avant le debut

# %%
def anomalie_fin_poste(df):
    #convert date columns to datetime
    df['DATE FIN DE FONCTION'] = pd.to_datetime(df['DATE FIN DE FONCTION'], errors='coerce')
    df['DATE DEBUT DE FONCTION'] = pd.to_datetime(df['DATE DEBUT DE FONCTION'], errors='coerce')
    # detect anomalies
    anomalie_df = df[df['DATE FIN DE FONCTION'] < df['DATE DEBUT DE FONCTION']]
    if len(anomalie_df) == 0:
        print("Tous les agents ont une date de fin de fonction valide (ceci n'est pas une anomalie !!!)")
    else:
        print(f"# {len(anomalie_df)} agents ont une anomalie de date de fin de fonction. Leur date de fin de fonction est inférieure à leur date de début de fonction.")
        
        

# %% [markdown]
# #### anomalie4 : les valeurs manquantes dans chaque colonne

# %%
def valeur_manquante(df):
    anomalie_valeur = df.isnull().sum()
    anomalie_valeur = anomalie_valeur[anomalie_valeur > 0]
    if len(anomalie_valeur) == 0:
        print("Aucune valeur manquante dans le fichier.")
    else:
        print(f"# {len(anomalie_valeur)} colonnes contiennent des valeurs manquantes.")
        print(anomalie_valeur)
        
    

# %% [markdown]
# il y'a beaucoup de colonne avec des valeurs manquantes sur ce jeux de données

# %% [markdown]
# #### anomalie5 : detecter les doublons

# %%
#=====detecter les doublons dans le fichier========
def anomalie_doublons(df) : 
    doublons = df.duplicated().sum()
    numero_employe = df['NUMERO EMPLPOYE'].duplicated().sum()
    if doublons == 0:
        print("Aucun doublon dans le fichier.")
    else:
        print(f"# {doublons} doublons trouvés dans le fichier.")
        
    if numero_employe == 0: 
        print("Aucun numéro d'employé en double dans le fichier.")
    else:
        print(f"# {numero_employe} numéros d'employé en double trouvés dans le fichier.")    



# %% [markdown]
# #### anomalie6 : les valeurs trop extemem comme les ages <18 ou > 65 les nb_enfants >10 ou nb_femmes > 4  

# %%
def anomalie6(data) :
    age = data['AGE']
    nb_enfants = data['NOMBRE ENFANT']
    femmes = data['NOMBRE EPOUSE']
    #age < 18 or age > 68
    anomalie_age = data[(age < 18) | (age > 68)]
    anomalie_nb_enfants = data[(nb_enfants < 0) | (nb_enfants > 10)]
    anomalie_nb_femmes = data[(femmes < 0) | (femmes > 4)]
    if len(anomalie_age) == 0:
        print("Aucun personnel n'a un age anormal.")
    else:
        print(f"# {len(anomalie_age)} agents ont un age anomale (soit inférieur à 18 ans soit supérieur à 68 ans).")
    if len(anomalie_nb_enfants) == 0:
        print("Aucun personnel n'a un nombre d'enfants anormal.")
    else:
        print(f"# {len(anomalie_nb_enfants)} agents ont un nombre d'enfants anomale (soit inférieur à 0 soit supérieur à 10).")  
    if len(anomalie_nb_femmes) == 0:
        print("Aucun personnel n'a un nombre d'épouses anormal.")
    else:
        print(f"# {len(anomalie_nb_femmes)} agents ont un nombre d'épouses anomale (soit inférieur à 0 soit supérieur à 4).")          




# %% [markdown]
# #### fonction pour detecter tous les anomalies a partir d'un fichier 

# %%
import os
import os
import io
import contextlib
import pandas as pd

def exporter_anomalies_personnel(fichier_entree ):
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
    fonctions_anomalies = [anomalie_recrutement, anomalie_retraite, anomalie_fin_poste , anomalie_doublons , anomalie6]

    # Rediriger la sortie print vers un fichier texte
    with open(nom_sortie, 'w', encoding='utf-8') as f:
        for i, fonction in enumerate(fonctions_anomalies, 1):
            f.write(f"===== Anomalie {i} =====\n")
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                fonction(data)
            f.write(buffer.getvalue())
            f.write("\n\n")
    print(f"Les anomalies  ont été exportées vers {nom_sortie}")
    

    



