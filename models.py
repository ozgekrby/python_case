from __init__ import db
from datetime import datetime

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500), nullable=False)
    options = db.Column(db.String(500), nullable=False)
    correct_answer = db.Column(db.String(100), nullable=False)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Score {self.username}: {self.score}>' 