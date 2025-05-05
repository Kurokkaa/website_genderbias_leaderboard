from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os
import pandas as pd
from model import db, LeaderboardEntry


# Flask initialization
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///leaderboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#----------------------------------------Pages----------------------------------------#
@app.route('/')
def accueil():
    return render_template('home.html')  # Assure-toi que le fichier index.html existe dans le répertoire templates

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['csv_file']
    
        data_type_select = request.form['data_type']
        model_name_select = request.form['model_name']
        leaderboard_select = request.form['leaderboard']

        if data_type_select == "gendered":
            gender_gap = calculate_gender_gap(file)
            gender_shift = calculate_gender_shift(file)
            if leaderboard_select == "yes":
                add_to_sql(model_name_select, data_type_select, gender_gap, file, gender_shift)
            return render_template('upload.html', result=True, gender_gap=gender_gap, gender_shift=gender_shift, leaderboard=leaderboard_select)
        
        elif data_type_select == "neutral":
            gender_gap = calculate_gender_gap(file)
            if leaderboard_select == "yes":
                add_to_sql(model_name_select, data_type_select, gender_gap, file, None)
            return render_template('upload.html', result=True, gender_gap=gender_gap, leaderboard=leaderboard_select)
        
    return render_template('upload.html')

@app.route('/leaderboard')
def leaderboard():
    entries = LeaderboardEntry.query.order_by(LeaderboardEntry.average.asc()).all()
    return render_template('leaderboard.html', leaderboard=entries)

@app.route('/about')
def about():
    return render_template('about.html')


#----------------------------------------Functions----------------------------------------#
def calculate_gender_gap(file):
    return 2
def calculate_gender_shift(file):
    return 5


def add_to_sql(modelname, genre, gendergap, file ,gendershift=None):
    if(gendergap<0):
        gg_fem = abs(gendergap)
        gg_masc = None
    else:
        gg_masc = gendergap
        gg_fem = None
    existing_model = LeaderboardEntry.query.filter_by(model=modelname).first()
    print(existing_model)
    if existing_model:
        # Update the existing entry if modelname already exists
        if genre == "neutral":
            existing_model.gg_masc_neutral = gg_masc
            existing_model.gg_fem_neutral = gg_fem
        elif genre == "gendered":
            existing_model.gg_masc_gendered = gg_masc
            existing_model.gg_fem_gendered = gg_fem
            existing_model.gender_shift = gendershift
        values = [
            existing_model.gg_masc_neutral,
            existing_model.gg_fem_neutral,
            existing_model.gg_masc_gendered,
            existing_model.gg_fem_gendered,
            existing_model.gender_shift
        ]
        numeric_values = [v for v in values if v is not None]
        existing_model.average = sum(numeric_values) / len(numeric_values) if numeric_values else 0

        db.session.commit()
        return
    
    entry_data = {
        "model": modelname,
        "average": 0,
        "gender_shift": gendershift if genre == "gendered" else None,
        "gg_masc_neutral": gg_masc if genre == "neutral" else None,
        "gg_fem_neutral": gg_fem if genre == "neutral" else None,
        "gg_masc_gendered": gg_masc if genre == "gendered" else None,
        "gg_fem_gendered": gg_fem if genre == "gendered" else None,
    }
    numeric_values = [v for v in [entry_data["gg_masc_neutral"], entry_data["gg_fem_neutral"], entry_data["gg_masc_gendered"], entry_data["gg_fem_gendered"], entry_data['gender_shift']] if v is not None]
    entry_data["average"] = sum(numeric_values) / len(numeric_values) if numeric_values else 0

    new_entry = LeaderboardEntry(**entry_data)
    db.session.add(new_entry)
    db.session.commit()

def initialize_database():
    db_path = 'instance/leaderboard.db'
    import sqlite3
    with open('init_db.sql', 'r') as f:
        init_script = f.read()
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.executescript(init_script)
    conn.commit()
    conn.close()
    print("✅ Updating database OK!")

#----------------------------------------Init----------------------------------------#
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    initialize_database()
    app.run(debug=True)
