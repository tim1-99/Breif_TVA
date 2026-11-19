
import requests
import csv
import pandas as pd
import time
import logging 

# stocke l'adresse du service VIES dans une variable appelée url
url = "https://ec.europa.eu/taxation_customs/vies/rest-api/ms/LU/vat/32431802"


#configuration logging pour enregistrer les information sur la requête 
logging.basicConfig(
    filename="collecte_vies.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)

logging.info("Début de la campagne VIES")

# Lire les données nettoyées
df = pd.read_csv("tva_nettoye.csv")

# Crée un DataFrame vide pour stocker les anciens résultats ça parmet de ne pas vérifier plusieurs fois les mêmes numéros de TVA.

anciens_resultats = pd.DataFrame()
try:
    #lire le fichier contenant les résultats précédents si le fichier existe, 
    anciens_resultats = pd.read_csv("resultats_vies.csv")
      # Récupère les numéros de TVA déjà vérifiés dans une liste
    numeros_deja_verifies = anciens_resultats["numero_tva"].tolist()

except FileNotFoundError:
 #sinon créer un list vide
    numeros_deja_verifies = []


df_test = df.head(200).copy()

# prepare un liste vide pour stocke le resultat 
resultats = []
#boucle for et iterrows  parcourir un DataFrame ligne par ligne.
for _, ligne in df_test.iterrows():

    numero = ligne["numero_normalise_tva"]
    pays = ligne["pays_declare"]
    # condition pour ignorer les numéros déjà vérifiés et permet d'accélérer la collecte
    if numero in numeros_deja_verifies:
     logging.info("Numéro %s déjà vérifié : appel ignoré", numero)
     continue

    # Construire l'adresse de l'API VIES
    url = f"https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{pays}/vat/{numero}"

    try:
        debut = time.time()
        reponse = requests.get(url, timeout=30)
        fin = time.time()
        duree = fin - debut 

        donnees = reponse.json()

        resultats.append({
            "numero_tva": numero,
            "pays": pays,
            "code_http": reponse.status_code,
            "isValid": donnees.get("isValid"),
            "nom": donnees.get("name"),
            "adresse": donnees.get("address"),
            "date": donnees.get("requestDate"),
            "temps_reponse": round(duree, 2),
            "debut": debut,
            "fin": fin
        })
        
        logging.info(
            "Numéro %s - Pays %s - HTTP %s - debut :%s - fin : %s- Temps : %.2f secondes",
            numero, pays, reponse.status_code, debut, fin ,duree
        )
        
# detecter les erreurs 
    except requests.RequestException as erreur:
        logging.error("Erreur pour le numéro %s : %s", numero, erreur)

   # pause de 5 seconde entre les requetes  
    time.sleep(5) 

 #construire un DataFrame à partir de la liste de résultats et concaténer avec les anciens résultats tous le resemble dans un seul DataFrame
df_resultats = pd.DataFrame(resultats)
# Ajouter les nouveaux résultats aux anciens
df_resultats = pd.concat(
    [anciens_resultats, df_resultats],
    ignore_index=True
)

 #Enregistrer les résultats dans le CSV
df_resultats.to_csv(
    "resultats_vies.csv",
    index=False,
    encoding="utf-8"
)
logging.info("Fin de la campagne VIES")
