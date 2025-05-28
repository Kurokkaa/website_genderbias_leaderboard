# Gender Bias Cover Letter Web App

Ce site web permet d’utiliser l’outil développé par **Fanny Ducel** dans le cadre de son stage, disponible sur [GitHub](https://github.com/FannyDucel/GenderBiasCoverLetter).

---

## Présentation

Cette application web fournit une interface pour analyser des lettres de motivation en détectant des biais de genre, grâce à l’outil développé par Fanny Ducel.

---

## Installation et lancement

### Prérequis

- **Docker** et **Docker Compose** doivent être installés sur votre machine.

### Lancement de l’application

Pour construire et lancer le site avec Docker Compose (recommandé) :

```bash
docker compose up --build
```

Pour lancer simplement le site (avec redémarrage automatique en cas de crash) :

```bash
docker compose up
```

Si vous préférez lancer sans Docker, vous pouvez utiliser :

```bash
python app.py
```

```bash
flask run
```

### Mise à jour des traductions

Les traductions sont stockées dans le dossier translations sous forme de fichiers .mo. Ces fichiers contiennent les variables utilisées dans les templates HTML.

Pour compiler ou mettre à jour les fichiers de traduction .mo, exécutez :

```bash
pybabel compile -d translations
```

### Initialisation de la base de données

Pour initialiser la base de données avec les données par défaut, décommentez "initialize_database()" dans le fichier app.py (dans la fonction main), puis lancez l’application.

Pensez à recommenter cette partie après initialisation afin de ne pas écraser les nouvelles données lors des prochains démarrages.

## Suppression d’entrées dans la base

Pour supprimer une entrée dans la base, utilisez le script removedb.py avec les arguments suivants :

[modelname] : nom du modèle

[table] : neutral ou gendered

```bash
python removedb.py [modelname] [table]
```

Utilisation du Docker Compose

Pour mettre à jour votre configuration Docker Compose en arrière-plan :

```bash
docker compose up -d
```

Pour arrêter le service :

```bash
docker compose down
```

## Licence

Ce projet est sous licence [à completer]
