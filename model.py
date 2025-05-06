from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class LeaderboardEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    average = db.Column(db.Float, nullable=False)
    gg_masc_neutral = db.Column(db.Float, nullable=True)
    gg_fem_neutral = db.Column(db.Float, nullable=True)
    gg_masc_gendered = db.Column(db.Float, nullable=True)
    gg_fem_gendered = db.Column(db.Float, nullable=True)
    gender_shift = db.Column(db.Float, nullable=True)

class LeaderboardEntry_neutral(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    gg_masc_neutral = db.Column(db.Float, nullable=True)
    gg_fem_neutral = db.Column(db.Float, nullable=True)

class LeaderboardEntry_gendered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    model = db.Column(db.String(100), nullable=False)
    gg_masc_gendered = db.Column(db.Float, nullable=True)
    gg_fem_gendered = db.Column(db.Float, nullable=True)
    gender_shift = db.Column(db.Float, nullable=True)
