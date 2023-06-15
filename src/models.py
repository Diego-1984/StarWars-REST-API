import os
import sys
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class People(db.Model):
    __tablename__ = 'people'
    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable = False)
    gender = db.Column(db.String(250))
    height = db.Column(db.Integer)
    hair_color = db.Column(db.String(250))
    eye_color = db.Column(db.String(250))
    birth_year = db.Column(db.Integer)
    basic_data_id = Column(Integer, ForeignKey('basic_data.id'), primary_key=True)

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "name": self.name,
            "description": self.description,
            "gender": self.gender,
            "height": self.height,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year
        }


class Planet(db.Model):
    __tablename__ = 'planet'

    id = db.Column(db.Integer, primary_key=True)
    image_url = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable = False)
    climate = db.Column(db.String(250))
    population = db.Column(db.Integer)
    diameter = db.Column(db.Integer)
    terrain = db.Column(db.String(250))
    surface_water = db.Column(db.Integer)
    orbital_period = db.Column(db.Integer)
    basic_data_id = Column(Integer, ForeignKey('basic_data.id'), primary_key=True)

    def __repr__(self):
        return '<Planet %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "image_url": self.image_url,
            "name": self.name,
            "description": self.description,
            "climate": self.climate,
            "population": self.population,
            "diameter": self.diameter,
            "terrain": self.terrain,
            "surface_water": self.surface_water
        }

class Favorites(Base):
    __tablename__ = 'favorite'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    basic_data_id = Column(Integer, ForeignKey('basic_data.id'), primary_key=True)

class basic_data(Base):
    __tablename__ = 'basic_data'
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    name = Column(String(250), nullable=False)
