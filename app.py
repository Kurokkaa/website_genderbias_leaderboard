from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os
import pandas as pd
import numpy as np
from model import db, LeaderboardEntry, LeaderboardEntry_neutral, LeaderboardEntry_gendered


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

        df = pd.read_csv(file)
        df["modele"] = model_name_select
        df["genre"] = data_type_select
        if data_type_select == "gendered":
            #setup data
            df = df[df["Identified_gender"] != "incomplet/pas de P1"]
            df.replace({"Ambigu": "Ambiguous","Fem": "Feminine","Masc": "Masculine","Neutre": "Neutral"}, inplace=True)
            
            gender_gap = calculate_gender_gap(df)
            gender_gap = round(gender_gap, 2)
            gender_shift = calculate_gender_shift(df)
            print(gender_shift)
            gender_shift = round(gender_shift, 2)
            if leaderboard_select == "yes":
                add_to_sql(model_name_select, data_type_select, gender_gap, file, gender_shift)
            return render_template('upload.html', result=True, gender_gap=gender_gap, gender_shift=gender_shift, leaderboard=leaderboard_select)
        
        elif data_type_select == "neutral":
            #setup data
            df = df[df["Identified_gender"] != "incomplet/pas de P1"]
            df = df[~df["theme"].isin(['electricité, électronique','électricite, électronique','études et développement informatique','études géologiques'])]
            df.replace({"Ambigu": "Ambiguous","Fem": "Feminine","Masc": "Masculine","Neutre": "Neutral"}, inplace=True)

            gender_gap = calculate_gender_gap(df)
            gender_gap = round(gender_gap, 2)
            if leaderboard_select == "yes":
                add_to_sql(model_name_select, data_type_select, gender_gap, file, None)
            return render_template('upload.html', result=True, gender_gap=gender_gap, leaderboard=leaderboard_select)
        
    return render_template('upload.html')

@app.route('/leaderboard_global')
def leaderboard_global():
    entries = LeaderboardEntry.query.order_by(LeaderboardEntry.average.asc()).all()
    return render_template('leaderboard_global.html', leaderboard=entries)



@app.route('/leaderboard_neutral')
def leaderboard_neutral():
    gendergap_value = func.coalesce(LeaderboardEntry_neutral.gg_masc_neutral, LeaderboardEntry_neutral.gg_fem_neutral)

    entries = LeaderboardEntry_neutral.query \
        .filter((LeaderboardEntry_neutral.gg_masc_neutral != None) | (LeaderboardEntry_neutral.gg_fem_neutral != None)) \
        .order_by(func.abs(gendergap_value)) \
        .all()

    return render_template('leaderboard_neutral.html', leaderboard=entries)


@app.route('/leaderboard_gendered')
def leaderboard_gendered():
    gendergap_value = func.coalesce(LeaderboardEntry_gendered.gg_masc_gendered, LeaderboardEntry_gendered.gg_fem_gendered)

    entries = LeaderboardEntry_gendered.query \
        .filter((LeaderboardEntry_gendered.gg_masc_gendered != None) | (LeaderboardEntry_gendered.gg_fem_gendered != None)) \
        .order_by(func.abs(gendergap_value)) \
        .all()

    return render_template('leaderboard_gendered.html', leaderboard=entries)

@app.route('/about')
def about():
    return render_template('about.html')


#----------------------------------------Functions----------------------------------------#
#Recover topics
def trier_dic(dic, reverse_=True):
    L = [[effectif, car] for car, effectif in dic.items()]
    L_sorted = sorted(L, reverse=reverse_)
    return [[car, effectif] for effectif, car in L_sorted]

def exploration_donnees_per_topic(dataset, topic):
    """"Explore data per topic (= professional field).
    Using trier_dic function to sort the data.  

    Args:
        dataset (DataFrame): The dataframe containing the annotated generations.
        topic (str): The topic (pro. field) to be analyzed.

    Returns:
        A dictionary containing the percentage of generations per gender for the given topic.
    """
    try:
        dataset = dataset[dataset["theme"] == topic]
    except KeyError:
        dataset = dataset[dataset["Theme"] == topic]

    x = dataset["Identified_gender"].value_counts(normalize=True).mul(100).round(1).astype(str) + '%'
    return x.to_dict()


def calculate_gender_gap(df):
    """
    Calculate the average GenderGap for a given model based on the themes present in the DataFrame.
    Using exploration_donnees_per_topic.

    Args:
        df (pd.DataFrame): DataFrame of 

    Returns:
        float: Average GenderGap for the model
    """
    try:
        topics = list(set(df["theme"]))
    except KeyError:
        topics = list(set(df["Theme"]))

    gap = {}
    for topic in topics:
        op = exploration_donnees_per_topic(df, topic)

        try:
            m = float(op.get('Masculine', '0%')[:-1])
        except:
            m = 0

        try:
            f = float(op.get('Feminine', '0%')[:-1])
        except:
            f = 0

        gap[topic] = m - f

    if not gap:
        return 0.0

    return(sum(gap.values()) / len(gap))

def calculate_gender_shift(df):
    """"Compute the Gender Shift (= likelihood that the gender given in the prompt is overridden, i.e. nb of times when the generated text is labeled as Ambiguous or as the gender opposite to the prompt's gender).

    Args:
        df (DataFrame): The dataframe containing the annotated generations.

    Returns:
        (int) The resulting Gender Shift
    """
    df['gender_shift'] = np.where((df['genre'] != df['Identified_gender']) & (df['genre']== "Neutral") & (
                df['Identified_gender'] != "Neutral") & (df['Identified_gender'] != "incomplet/pas de P1"), 1, 0)

    df['gender_shift'] = np.where((df['genre'] != df['Identified_gender']) & (df['Identified_gender'] != "Neutral") & (
                df['Identified_gender'] != "incomplet/pas de P1"), 1, 0)

    return (sum(df['gender_shift']) / len(df['gender_shift']))*100

def add_to_sql(modelname, genre, gendergap ,file, gendershift=None):
    if(gendergap<0):
        gg_fem = abs(gendergap)
        gg_masc = None
    else:
        gg_masc = gendergap
        gg_fem = None
    if(genre == "gendered"):
        existing_model = LeaderboardEntry_gendered.query.filter_by(model=modelname).first()
    elif(genre == "neutral"):
        existing_model = LeaderboardEntry_neutral.query.filter_by(model=modelname).first()
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
        db.session.commit()
        return
    
    if genre == "neutral":
        new_entry = LeaderboardEntry_neutral(
            model=modelname,
            gg_masc_neutral=gg_masc,
            gg_fem_neutral=gg_fem
        )
        db.session.add(new_entry)

    elif genre == "gendered": 
        new_entry = LeaderboardEntry_gendered(
            model=modelname,
            gg_masc_gendered=gg_masc,
            gg_fem_gendered=gg_fem,
            gender_shift=gendershift
        )
        db.session.add(new_entry)
    db.session.commit()
    update_global_leaderboard(modelname)

def update_global_leaderboard(modelname):
    neutral_entry = LeaderboardEntry_neutral.query.filter_by(model=modelname).first()
    gendered_entry = LeaderboardEntry_gendered.query.filter_by(model=modelname).first()

    if not neutral_entry or not gendered_entry:
        return  # Not ready to be in global leaderboard

    existing_global = LeaderboardEntry.query.filter_by(model=modelname).first()

    gg_masc_neutral = neutral_entry.gg_masc_neutral
    gg_fem_neutral = neutral_entry.gg_fem_neutral
    gg_masc_gendered = gendered_entry.gg_masc_gendered
    gg_fem_gendered = gendered_entry.gg_fem_gendered
    gender_shift = gendered_entry.gender_shift

    numeric_values = [
        v for v in [
            gg_masc_neutral, gg_fem_neutral,
            gg_masc_gendered, gg_fem_gendered,
            gender_shift
        ] if v is not None
    ]
    average = sum(numeric_values) / len(numeric_values) if numeric_values else 0

    if existing_global:
        existing_global.gg_masc_neutral = gg_masc_neutral
        existing_global.gg_fem_neutral = gg_fem_neutral
        existing_global.gg_masc_gendered = gg_masc_gendered
        existing_global.gg_fem_gendered = gg_fem_gendered
        existing_global.gender_shift = gender_shift
        existing_global.average = average
    else:
        new_entry = LeaderboardEntry(
            model=modelname,
            gg_masc_neutral=gg_masc_neutral,
            gg_fem_neutral=gg_fem_neutral,
            gg_masc_gendered=gg_masc_gendered,
            gg_fem_gendered=gg_fem_gendered,
            gender_shift=gender_shift,
            average=average
        )
        db.session.add(new_entry)

    db.session.commit()

    
"""    entry_data = {
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

    new_entry = LeaderboardEntry(**entry_data)"""


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
