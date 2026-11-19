# Breif_TVA
Le déroulement breif 
1. Explorer les données
   Ouvrir le fichier et regarder ce qu'il contient : pays, numéros_tva, ...
 1.1 lire les donnes avec la fonction  et repondre la la question 
1. Nettoyer les données
   2.1-J'ai utilisé la fonction normaliser() du module validation_structure.py pour uniformiser les numéros TVA : suppression des espaces et des caractères inutiles, et mise en majuscules.
2. Vérifier la structure
   3.1-J'ai utilisé la fonction valider() pour vérifier la structure des numéros TVA et obtenir un verdict accompagné d'un motif.
   J'ai conservé les numéros ayant le verdict ok et écarté les numéros qui ne répondaient pas aux critères structurels.
    3.2-Suppression des doublons
    J'ai utilisé drop_duplicates() sur la colonne numero_normalise_tva afin de supprimer les numéros identiques après normalisation.
  3.4- Résultat
   Après ces étapes de nettoyage et de suppression des doublons, j'ai obtenu 5 802 numéros TVA uniques et structurellement valides.
   enregistre le resultat dans un fichier CSV
1. Interroger l'API VIES
   Créer script.py devrais automatise la verification 
   lire le fichier nettoye 
   Sélectionner les 200 premiers
   configuration logging pour enregistrer les information sur la requête 
   Interroger VIES numéro par numéro
   trier les donnes 
   Récupérer et stocker les réponses dans la liste resultat 
   affichier le resultat dans fichier csv 
2. Analyser les résultats
   Compter les numéros valides, invalides et non vérifiés, puis créer des graphiques.




# reponse des question phase 2: 
Combien d'appels votre nettoyage vous a-t-il fait économiser ?
Grâce au nettoyage et à la suppression des doublons, j'ai réduit le nombre de numéros à vérifier de 10 000 à 5 802. J'ai donc économisé 4 198 appels à l'API VIES.

# reponse des question phase 3:
 votre échantillon de deux cents numéros représente-t-il le référentiel ? 
Il ne garantit pas une représentation équilibrée des différents pays. Les résultats permettent de tester le fonctionnement de l'API VIES
Comment l'avez-vous tiré ?
J'ai sélectionné les 200 premières lignes du fichier après nettoyage et suppression des doublons.
Une fois une réponse obtenue, combien de temps reste-t-elle vraie : un numéro vérifié il y a six mois doit-il être revérifié avant la prochaine facture ?
oui, il faut verifier car la situation de l'entreprise peut changer.