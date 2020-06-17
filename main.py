"""
This module run a microservice called Space service. This module
manage all logic for wys Spaces

"""

import jwt
import os
import logging
import constants
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

class Category(db.Model):
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

class Subcategory(db.Model):
    """
    Subcategory.
    Represent a Subcategory of Spaces that are used to calc the final area.

    Attributes
    ----------
    id: Represent the unique id of a Internal SubCategory
    name: Name of a Internal Category
    category_id: Parent Category's ID (Many to One)
    spaces: Spaces associated to this subcategory (One to Many)
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    area = db.Column(db.Float)
    people_capacity = db.Column(db.Float)
    usage_percentage = db.Column(db.Float)
    unit_area = db.Column(db.Float)
    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)
    spaces = db.relationship(
        "Space",
        backref="subcategory")

    def serialize(self):
        """
        Serialize to json
        """
        return jsonify(self.to_dict())

    def to_dict(self):
        """
        Convert to dictionary
        """

        spaces_dicts = [space.to_dict()
                                for space in self.spaces]
        obj_dict = {
            'id': self.id,
            'name': self.name,
            'area': self.area,
            'people_capacity': self.people_capacity,
            'category_id': self.category_id,
            'spaces' : spaces_dicts
        }

        return obj_dict

class Space(db.Model):
    """
    Space.
    Represent a WYS Space structure for save in db.

    Attributes
    ----------
    id: Represent the unique id of a Space
    name: Name of the Space
    ...
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    model_2d = db.Column(db.BLOB)
    model_3d = db.Column(db.BLOB)
    height = db.Column(db.Float, nullable=False)
    width =  db.Column(db.Float, nullable=False)
    active =  db.Column(db.Boolean, default = True)
    regular =  db.Column(db.Boolean, nullable=False)
    up_gap =  db.Column(db.Float, default = 0)
    down_gap =  db.Column(db.Float, default = 0)
    left_gap = db.Column(db.Float, default = 0)
    right_gap = db.Column(db.Float, default = 0)
    subcategory_id = db.Column(db.Integer, db.ForeignKey(
        'subcategory.id'), nullable=False)

    def to_dict(self):
        """
        Convert to dictionary
        """

        obj_dict = {
            'id': self.id,
            'name': self.name,
            'model_2d' : self.model_2d,
            'model_3d' : self.model_3d,
            'height' : self.height,
            'width' :  self.width,
            'active' :  self.active,
            'regular' :  self.regular,
            'up_gap' :  self.up_gap,
            'down_gap' :  self.down_gap,
            'left_gap' : self.left_gap,
            'right_gap' : self.right_gap,
            'subcategory_id' : self.subcategory_id
        }

        return obj_dict

    def serialize(self):
        """
        Serialize to json
        """
       
        return jsonify(self.to_dict())

db.create_all() # Create all tables

def load_constants_seed_data():
    
    cat_total_rows = db.session \
        .query(Category) \
        .count()
    
    subcat_total_rows = db.session \
        .query(Subcategory) \
        .count()
    
    # If there are variables in database, do nothing
    if(cat_total_rows > 0 and subcat_total_rows > 0):
        return
    
    # Else put the variables by defect

    try:
        for k, v in constants.SEED_DATA.items():
            category = Category(name=k)
            for i, j in v.items():
                subcategory = Subcategory( name = i, 
                                           area = j['SUPERFICIE'],
                                           people_capacity = j['PERSONAS'], 
                                           usage_percentage = j['PORC_USO'], 
                                           unit_area = j['SUPERFICIE_U'])
                category.subcategories.append(subcategory)
            db.session.add(category)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"load_constants_seed_data -> {e}")

# Swagger Config

SWAGGER_URL = '/api/spaces/docs/'
API_URL = '/api/spaces/spec'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "WYS Api. Space Service"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = request.headers.get('Authorization', None)
        if not token:
            app.logger.debug("token_required")
            return jsonify({'message': 'a valid token is missing'})
        app.logger.debug("Token: " + token)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return jsonify({'message': 'token is invalid'})

        return f(*args, **kwargs)

    return decorator


@app.route("/api/spaces/spec", methods=['GET'])
@token_required
def spec():
    return jsonify(swagger(app))








@app.route('/api/spaces/<space_id>', methods = ['GET', 'PUT', 'DELETE'])
@token_required
def manage_space_by_id(space_id):
    """
        Manage Space By ID (Show, update and delete)
        ---
        parameters:
          - in: path
            name: space_id
            type: integer
            description: Space ID
        responses:
          200:
            description: Space Object or deleted message
          404:
            description: Space Not Found
          500:
            description: "Database error"
    """
    try:
        space = Space.query.filter_by(id=space_id).first()
        if(space is not None):
            if request.method == 'GET':
                return space.serialize(), 200
            if request.method == 'PUT':
                space.name = request.json['name'] if 'name' in request.json else space.name
                space.model_2d = request.json['model_2d'] if 'model_2d' in request.json else space.model_2d
                space.model_3d = request.json['model_3d'] if 'model_3d' in request.json else space.model_3d
                space.height = request.json['height'] if 'height' in request.json else space.height
                space.width =  request.json['width'] if 'width' in request.json else space.width
                space.regular =  request.json['regular'] if 'regular' in request.json else space.regular
                space.up_gap =  request.json['up_gap'] if 'up_gap' in request.json else space.up_gap
                space.down_gap =  request.json['down_gap'] if 'down_gap' in request.json else space.down_gap
                space.left_gap = request.json['left_gap'] if 'left_gap' in request.json else space.left_gap
                space.right_gap = request.json['right_gap'] if 'right_gap' in request.json else space.right_gap

                db.session.commit()

                space_updated = Space.query.filter_by(id=space_id).first()
                
                return space_updated.serialize(), 200

            if request.method == 'DELETE':
                space.active = False
                db.session.commit()

                return jsonify({'result': 'Space deactivated'}), 200

        return '{}', 404
    except Exception as exp:
        app.logger.error(f"Error in database: mesg ->{exp}")
        return exp, 500

if __name__ == '__main__':
    load_constants_seed_data()
    app.run()
    app.debug=True