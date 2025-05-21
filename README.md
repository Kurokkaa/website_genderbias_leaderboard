## Contexte 

Ce site web sert à utiliser l'outil créé par Fanny Ducel, dans le cadre d'un stage. (https://github.com/FannyDucel/GenderBiasCoverLetter)

# Executer pour lancer le site web :
python app.py ou flask run

# Pour mettre à jour les traductions ou ajouter une nouvelle langue ou de nouveau textes :

pybabel compile -d translations

# Pour supprimer une entrée dans le site web :

[modelname] : nom du modèle
[table] : neutral ou gendered

"python removedb.py [modelname] [table]"
