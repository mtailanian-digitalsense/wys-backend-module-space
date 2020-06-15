"""
This module run a microservice called Project service. This module
manage all logic for wys projects

"""

import jwt
import os
import logging
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps

# Loading Config Parameters
DB_USER = os.getenv('DB_USER', 'wys')
DB_PASS = os.getenv('DB_PASSWORD', 'rac3e/07')
DB_IP = os.getenv('DB_IP_ADDRESS', '10.2.19.195')
DB_PORT = os.getenv('DB_PORT', '3307')
DB_SCHEMA = os.getenv('DB_SCHEMA', 'wys')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_SCHEMA}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY']= 'Th1s1ss3cr3t'
app.logger.setLevel(logging.DEBUG)
db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run()
    app.debug=True

class Category(db.model):
    """
    Category.
    Represent a Categories of Spaces that are used to calc the final area.

    Attributes
    ----------
    id: Represent the unique id of a Category
    name: Name of a Category
    subcategories: Subcategories associated to this category (One to Many)
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    subcategories = db.relationship(
        "Subcategory",
        backref="category")

    def to_dict(self):
        """
        Convert to dictionary
        """

        subcategories_dicts = [subcategory.to_dict()
                                for subcategory in self.subcategories]

        obj_dict = {
            'id': self.id,
            'name': self.name,
            'subcategories': subcategories_dicts}

        return obj_dict
    
    def serialize(self):
        """
        Serialize to json
        """
        return jsonify(self.to_dict())

class Subcategory(db.model):
    """
    Subcategory.
    Represent a Subcategory of Spaces that are used to calc the final area.

    Attributes
    ----------
    id: Represent the unique id of a Internal SubCategory
    name: Name of a Internal Category
    category_id: Parent Category's ID (Many to One)
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    area = db.Column(db.Float)
    people_capacity = db.Column(db.Float)
    usage_percentage = db.Column(db.Float)
    unit_area = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)

    def serialize(self):
        """
        Serialize to json
        """
        return jsonify(self.to_dict())

    def to_dict(self):
        """
        Convert to dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'density': self.density,
            'category_id': self.category_id
        }

class Space(db.Model):
    """
    Space.
    Represent a WYS Space structure for save in db.

    Attributes
    ----------
    id: Represent the unique id of a project
    name: Name of the project
    m2_id: Id of the work made in M2 module
    location_id: ID of the work made in location module

    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model_2d = db.Column(db.BLOB, nullable=False)
    model_3d = db.Column(db.BLOB, nullable=False)
    height = db.Column(db.Float, nullable=False)
    width =  db.Column(db.Float, nullable=False)
    active =  db.Column(db.Boolean, default = True)
    regular =  db.Column(db.Boolean, nullable=False)
    up_gap =  db.Column(db.Float, default = 0)
    down_gap =  db.Column(db.Float, default = 0)
    left_gap = db.Column(db.Float, default = 0)
    right_gap = db.Column(db.Float, default = 0)

    def to_dict(self):
        """
        Convert to dictionary
        """
        dict = {
            'id': self.id,
            'model_2d' : self.model_2d,
            'model_3d' : self.model_3d,
            'height' : self.height,
            'width' :  self.width,
            'active' :  self.active,
            'regular' :  self.regular,
            'up_gap' :  self.up_gap,
            'down_gap' :  self.down_gap,
            'left_gap' : self.left_gap,
            'right_gap' : self.right_gap
        }
        return dict

    def serialize(self):
        """
        Serialize to json
        """
       
        return jsonify(self.to_dict())

db.create_all() # Create all tables

# Swagger Config

SWAGGER_URL = '/api/projects/docs/'
API_URL = '/api/projects/spec'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "WYS Api. Project Service"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)
