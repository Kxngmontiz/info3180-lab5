# Add any model classes for Flask-SQLAlchemy here
from . import db

# Add any model classes for Flask-SQLAlchemy here

class Movie(db.Model):
    
    __tablename__ = "movies"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    poster = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime)
    