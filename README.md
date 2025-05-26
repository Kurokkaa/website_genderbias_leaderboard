## Contexte 

Ce site web sert à utiliser l'outil créé par Fanny Ducel, dans le cadre d'un stage. (https://github.com/FannyDucel/GenderBiasCoverLetter)

# Executer pour lancer le site web :
python app.py ou flask run

# Pour mettre à jour les traductions ou ajouter une nouvelle langue ou de nouveaux textes :
Changer les fichiers .mo dans translations (les variables contenues dans ces fichiers sont appelées dans les fichiers HTML du dossier templates).

pybabel compile -d translations



# Pour supprimer une entrée dans le site web :

[modelname] : nom du modèle
[table] : neutral ou gendered

"python removedb.py [modelname] [table]"
