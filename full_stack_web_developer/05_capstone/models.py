import os
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.environ.get(
    'DATABASE_URL', "postgres://{}/{}".format('localhost:5432', database_name))

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


'''
Actor

'''


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer)
    gender = Column(String)
    movies = db.relationship('Documentation', backref="Movie", lazy=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }


'''
Movie

'''


class Movie(db.Model):
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(String, nullable=False, default='unknown')
    actors = db.relationship('Documentation', backref="Actor", lazy=True)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
        }


'''
Documentation

'''


class Documentation(db.Model):
    __tablename__ = 'Documentation'

    id = db.Column(db.Integer, primary_key=True)
    actor_id = db.Column(db.Integer, db.ForeignKey('Actor.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movie.id'), nullable=False)
    role = db.Column(db.String(80), nullable=False, default="unknown")
