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

session_instance = db.session


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
        return render_template('upload.html', result=True, gender_gap=gender_gap, gender_shift=gender_shift, leaderboard=add_to_leaderboard)
    return render_template('upload.html')
@app.route('/leaderboard')
def leaderboard():
    entries = LeaderboardEntry.query.order_by(LeaderboardEntry.average.asc()).all()
    return render_template('leaderboard.html', leaderboard=entries)

@app.route('/about')
def about():
    return render_template('about.html')


#----------------------------------------Functions----------------------------------------#
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
