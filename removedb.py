import sys
from flask import Flask
from model import db, LeaderboardEntry, LeaderboardEntry_neutral, LeaderboardEntry_gendered

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def delete_model(model_name, table_name):
    with app.app_context():
        deleted = False

        if table_name == "neutral":
            entry = LeaderboardEntry_neutral.query.filter_by(model=model_name).first()
            if entry:
                db.session.delete(entry)
                db.session.commit()
                print(f"Modèle '{model_name}' supprimé de la table 'neutral'.")
                deleted = True

        elif table_name == "gendered":
            entry = LeaderboardEntry_gendered.query.filter_by(model=model_name).first()
            if entry:
                db.session.delete(entry)
                db.session.commit()
                print(f"✅ Modèle '{model_name}' supprimé de la table 'gendered'.")
                deleted = True
        else:
            print("Nom de table invalide. Utilisez 'neutral', 'gendered' ou 'global'.")
            return

        # Suppression conditionnelle dans la table globale si l'entrée n'existe plus dans l'une des autres
        if table_name in ["neutral", "gendered"] and deleted:
            neutral_entry = LeaderboardEntry_neutral.query.filter_by(model=model_name).first()
            gendered_entry = LeaderboardEntry_gendered.query.filter_by(model=model_name).first()
            if not neutral_entry or not gendered_entry:
                global_entry = LeaderboardEntry.query.filter_by(model=model_name).first()
                if global_entry:
                    db.session.delete(global_entry)
                    db.session.commit()
                    print(f"Entrée également supprimée de la table 'global' car elle est incomplète.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Utilisation : python removedb.py \"nom_du_modele\" \"table\"")
    else:
        model_name = sys.argv[1]
        table_name = sys.argv[2].lower()
        delete_model(model_name, table_name)
