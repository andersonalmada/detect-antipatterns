from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Alert(db.Model):
    __tablename__ = "alerts"
    
    id = db.Column(db.Integer, primary_key=True)
    host = db.Column(db.String, nullable=True)
    name = db.Column(db.String, nullable=False)
    service = db.Column(db.String, nullable=True)
    severity = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    value = db.Column(db.String, nullable=False)
