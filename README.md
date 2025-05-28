## Contexte 

Ce site web sert à utiliser l'outil créé par Fanny Ducel, dans le cadre d'un stage. (https://github.com/FannyDucel/GenderBiasCoverLetter)

# Mise en place 

il faut avoir installer docker puis:

"docker compose up --build" 


# Pour mettre à jour les traductions ou ajouter une nouvelle langue ou de nouveaux textes (lancer à la mise en place du site):
Changer les fichiers .mo dans translations (les variables contenues dans ces fichiers sont appelées dans les fichiers HTML du dossier templates).

pybabel compile -d translations

# Pour initialiser la base de donnée par défaut il faut enlever le commentaire dans le main du fichier app.py et lancer le démarrage, pensez à recommenter pour garder les nouvelles données dans la db

# Executer pour lancer le site web :

alors via le docker permettant le redémarrage automatique lors des crashs

"docker compose up" (conseillé)

sinon si il y a des problèmes, il est aussi possible d'éxecuter :

"python app.py" ou "flask run"

# Pour supprimer une entrée dans le site web :

[modelname] : nom du modèle
[table] : neutral ou gendered

"python removedb.py [modelname] [table]"


# pour mettre à jour le docker-compose.yml
"docker compose up -d"
