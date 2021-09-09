"""
This module run a microservice called Space service. This module
manage all logic for wys Spaces

"""

import jwt, os, logging, constants
from sqlalchemy.exc import SQLAlchemyError
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint
from functools import wraps
from sqlalchemy.ext.hybrid import hybrid_property
from flask_cors import CORS
from PIL import Image
import requests
from io import BytesIO
import json
import base64
from shapely.geometry.polygon import Polygon

# Loading Config Parameters
DB_USER = os.getenv('DB_USER', 'wys')
"""Config Parameters"""
DB_PASS = os.getenv('DB_PASSWORD', 'rac3e/07')
"""Config Parameters"""
DB_IP = os.getenv('DB_IP_ADDRESS', '10.2.14.195')
"""Config Parameters"""
DB_PORT = os.getenv('DB_PORT', '3307')
"""Config Parameters"""
DB_SCHEMA = os.getenv('DB_SCHEMA', 'wys')
"""Config Parameters"""
APP_HOST = os.getenv('APP_HOST', '127.0.0.1')
"""Config Parameters"""
APP_PORT = os.getenv('APP_PORT', 5002)
"""Config Parameters"""

# Buildings module info
BUILDINGS_MODULE_HOST = os.getenv('BUILDINGS_MODULE_HOST', '127.0.0.1')
""" Connect with building module"""
BUILDINGS_MODULE_PORT = os.getenv('BUILDINGS_MODULE_PORT', 5004)
""" Connect with building module"""
BUILDINGS_MODULE_API = os.getenv('BUILDINGS_MODULE_API', '/api/buildings/')
""" Connect with building module"""
BUILDINGS_URL = f"http://{BUILDINGS_MODULE_HOST}:{BUILDINGS_MODULE_PORT}"
""" Connect with building module"""

# Flask Configurations
app = Flask(__name__)
""" Flask configuration"""
CORS(app)

# SQL Alchemy Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{DB_USER}:{DB_PASS}@{DB_IP}:{DB_PORT}/{DB_SCHEMA}"
"""SQL Alchemy database uri configuration"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

try:
    f = open('oauth-public.key', 'r')
    key: str = f.read()
    f.close()
    app.config['SECRET_KEY'] = key
except Exception as terr:
    app.logger.error(f'Can\'t read public key f{terr}')
    exit(-1)

app.logger.setLevel(logging.DEBUG)
db = SQLAlchemy(app)
"""var with SQLAlchemy object"""

m_px = 3779.57517575025

class Category(db.Model):
    """
    Category
    ---
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
    Subcategory
    ---
    Represent a Subcategory of Spaces that are used to calc the final area.

    Attributes
    ----------
    id: Represent the unique id of a Internal SubCategory
    name: Name of a Internal Category
    area: Area related to a Subcategory
    people_capacity: People capacity asigned to a Subcategory
    usage_percentage: Usage percentage asigned to a Subcategory
    unit_area: Unit area related to a Subcategory
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

        spaces_dicts = [{"id": space.id}
                                for space in self.spaces]
        obj_dict = {
            'id': self.id,
            'name': self.name,
            'area': self.area,
            'people_capacity': self.people_capacity,
            'usage_percentage': self.usage_percentage,
            'unit_area': self.unit_area,
            'category_id': self.category_id,
            'spaces' : spaces_dicts
        }

        return obj_dict

class Space(db.Model):
    """
    Space
    ---
    Represent a WYS Space structure for save in db.

    Attributes
    ----------
    id: Represent the unique id of a Space
    name: Name of the Space
    __model_2d: BLOB of the 2D-model 
    __model_3d: BLOB of the 3D-model 
    height: space's height
    width: space's width
    active: boolean, if it's an active space
    regular: boolean, if it's a regular space
    up_gap: Space's up gap, in cms (holgura)
    down_gap: Space's down gap, in cms (holgura)
    left_gap: Space's left gap, in cms (holgura)
    right_gap: Space's right gap, in cms (holgura)
    subcategory_id: Subcategory id related
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    __model_2d = db.Column(db.BLOB)
    __model_3d = db.Column(db.BLOB)
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
    points = db.relationship(
        "Point",
        backref="space")

    def __init__(self, name, model_2d, model_3d, height, width,
                 regular, active=True, up_gap=0, down_gap=0, left_gap=0, right_gap=0, subcategory_id=0):
        self.name = name
        self.model_2d = model_2d
        self.model_3d = model_3d
        self.height = height
        self.width = width
        self.active = active
        self.regular = regular
        self.up_gap = up_gap
        self.down_gap = down_gap
        self.left_gap = left_gap
        self.right_gap = right_gap
        self.subcategory_id = subcategory_id

    @hybrid_property
    def model_2d(self):
        '''
        If there's model_2D saved, it's decoded and sent
        '''
        if self.__model_2d is not None:
            return self.__model_2d.decode('utf-8')
        else:
            return None

    @model_2d.setter
    def model_2d(self, model):
        if model is not None:
            self.__model_2d = model.encode('utf-8')
        else:
            self.__model_2d = None

    @hybrid_property
    def model_3d(self):
        '''
        If there's model_3D saved, it's decoded and sent
        '''
        if self.__model_3d is not None:
            return self.__model_3d.decode('utf-8')
        else:
            return None

    @model_3d.setter
    def model_3d(self, model):
        if model is not None:
            self.__model_3d = model.encode('utf-8')
        else:
            self.__model_3d = None

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
            'points': [point.to_dict() for point in self.points],
            'subcategory_id' : self.subcategory_id
        }
        
        return obj_dict

    def serialize(self):
        """
        Serialize to json
        """
        space_dict = self.to_dict()
        return jsonify(space_dict)

class Point(db.Model):
    """
    Point.
    ---
    Represents the ordered pair of a vertex of an irregular space.

    Attributes
    ----------
    id: Represent the unique id of a Point
    x: X coordinate of the vertex
    y: Y coordinate of the vertex
    order: Number of the order corresponding to the ordered pair
    space_id: Parent Space's ID (Many to One)
    """

    id = db.Column(db.Integer, primary_key=True)
    x = db.Column(db.Float, nullable=False)
    y =  db.Column(db.Float, nullable=False)
    order =  db.Column(db.Integer, nullable=False)
    space_id = db.Column(db.Integer, db.ForeignKey('space.id'), nullable=False)

    def to_dict(self):
        """
        Convert to dictionary
        """

        obj_dict = {
            'id': self.id,
            'x': self.x,
            'y': self.y,
            'order': self.order,
            'space_id': self.space_id}

        return obj_dict
    
    def serialize(self):
        """
        Serialize to json
        """
        return jsonify(self.to_dict())


db.create_all() # Create all tables


def load_constants_seed_data():
    '''
    To load constants values, it could be DB values or code constants values. 
    '''
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
load_constants_seed_data()


def token_required(f):
    """Function to get the token for the swagger"""
    @wraps(f)
    def decorator(*args, **kwargs):

        bearer_token = request.headers.get('Authorization', None)
        try:
            token = bearer_token.split(" ")[1]
        except Exception as ierr:
            app.logger.error(ierr)
            abort(jsonify({'message': 'a valid bearer token is missing'}), 500)

        if not token:
            app.logger.debug("token_required")
            return jsonify({'message': 'a valid token is missing'})

        app.logger.debug("Token: " + token)
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],
                              algorithms=['RS256'], audience="1")
            user_id: int = data['user_id']
            request.environ['user_id'] = user_id
        except Exception as err:
            return jsonify({'message': 'token is invalid', 'error': err})
        except KeyError as kerr:
            return jsonify({'message': 'Can\'t find user_id in token', 'error': kerr})

        return f(*args, **kwargs)

    return decorator


@app.route("/api/spaces/spec", methods=['GET'])
@token_required
def spec():
    """To load the swagger app"""
    swag = swagger(app)
    swag['info']['version'] = "1.0"
    swag['info']['title'] = "WYS Space API Service"
    swag['tags'] = [{
        "name": "spaces",
        "description": "Methods to configure spaces"
    },{
        "name": "spaces/subcategories",
        "description": "Methods to configure spaces subcategories"
    },{
        "name": "spaces/points",
        "description": "Methods to configure spaces points"
    }]
    return jsonify(swag)

class FloorLocation:
    """Spatial location of modules
    ___
    """

    def __init__(self):
        self.width_m = 0.0
        self.height_m = 0.0
        self.x_0 = 0
        self.y_0 = 0
        self.x_pixel_m = 0
        self.y_pixel_m = 0

    def to_dict(self):
        """
        Convert to dictionary
        """
        return {
            'width_m': self.width_m,
            'height_m': self.height_m,
            'x_pixel_m': self.x_pixel_m,
            'y_pixel_m': self.y_pixel_m
        }  
class SpaceLocation:
    """Spatial location of modules
    ___

    """

    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        self.width_p = 0
        self.height_p = 0
        self.rotation = 0
        self.space_id = 0
        self.image = ""

    def to_dict(self):
        """
        Convert to dictionary
        """
        return {
            'position_x': self.position_x,
            'position_y': self.position_y,
            'width': self.width_p,
            'height': self.height_p,
            'rotation': self.rotation,
            'space_id': self.space_id,
            'image': self.image
        }
def get_image_size(link):
    """
    Get the size of a image in pixels
    ___
    parameters:

        link: link of a image

    return:

        width and height in pixels
    """

    # Get image from internet
    try:
        resp = requests.get(link)
        image: Image = Image.open(BytesIO(resp.content))
        return image.width, image.height

    except Exception as e:
        raise e


def get_extremes_m(polygons: []):
    """
    Returns the extremes points in meters
    ___
    parameters:

        polygons: list with all floor polygons

    return:

        extreme points in meters.
    """
    width = 0.0
    height = 0.0
    points = []

    x_coords = []
    y_coords = []

    for pol in polygons:
        points += pol['points']

    for point in points:
        # Get all X points and save in a list
        x_coords.append(point['x'])
        # Get all Y points and save in a list
        y_coords.append(point['y'])

    # Getting max and min points

    x_max = max(x_coords)
    y_max = max(y_coords)

    x_min = min(x_coords)
    y_min = min(y_coords)

    return x_min, y_min, x_max, y_max
  
def init_floor(floor_dict: dict):
    """ Return the location of objects in the floor
    parameters:

        floor_dict: data given to smart layout

    return:

        FloorLocation object
    """

    # Init floor
    floor_loc = FloorLocation()

    # Polygons or elements of floor

    floor_polygons = floor_dict['selected_floor']['polygons']

    # Give width and length of a floor

    x_min, y_min, x_max, y_max = get_extremes_m(floor_polygons)

    floor_loc.width_m = (x_max - x_min) / 100.0
    floor_loc.height_m = (y_max - y_min) / 100.0

    # Give give the most left/up point
    floor_loc.x_0, floor_loc.y_0 = x_min / 100.0, y_max / 100.0

    # Get Pixel/Meters relation for a floor
    try:

        width_p, height_p = get_image_size(floor_dict['selected_floor']['image_link'])

    except Exception as e:
        raise e

    floor_loc.x_pixel_m = width_p * 1.0 / floor_loc.width_m  # pixels/meters
    floor_loc.y_pixel_m = height_p * 1.0 / floor_loc.height_m  # pixels/meters

    return floor_loc

'''
def transform_coords(floor_dict: dict, coordinates: []):
    """Transform coordinates into pixels
    ___
    parameters:
        floor_dict: data given to smart layout
        coordinates: list of all spaces with their coordinates

    return:

        spaces and floor elements with their coordinates in pixels
    """
    # Init floor
    floor_loc = init_floor(floor_dict)

    # build a dictionary of type of spaces
    spaces_dict = {}
    for space in floor_dict['workspaces']:
        spaces_dict[space['name']] = space

    # Save spaces here
    spaces = []

    # Read all spaces given by smart layout
    for space in coordinates:
        space_loc = SpaceLocation()
        space_name = space[0]
        xpos_m = space[2]
        ypos_m = space[3]
        rot = space[4]

        # (point_m - origin) multiplied for the pixel/meters reason.
        space_loc.position_x = (xpos_m - floor_loc.x_0) * floor_loc.x_pixel_m

        # Y coordinate is always positive
        space_loc.position_y = (ypos_m - floor_loc.y_0) * -1 * floor_loc.y_pixel_m
        space_loc.rotation = rot

        # Resizing image

        # Get width and height in meters
        space_info = spaces_dict[space_name]

        space_width_m = space_info['width']
        space_height_m = space_info['height']

        space_width_p = space_width_m * floor_loc.x_pixel_m
        space_height_p = space_height_m * floor_loc.y_pixel_m

        space_loc.width_p = space_width_p
        space_loc.height_p = space_height_p


        spaces.append(space_loc.to_dict())
    

    return spaces

'''

@app.route('/api/spaces/create', methods=['GET'])
@token_required
def data_to_create_spaces():
    """
        Show all categories and workspaces to be related to a space
        ---
        produces:

            - "application/json"

        tags:

            - "spaces"

        responses:

            200:
                description: A list of all categories and workspaces
            500:
                description: Internal Error

    """
    try:
        all_spaces_dicts = [space.to_dict() for space in Category.query.all()]
        return jsonify(all_spaces_dicts)
    except Exception as e:
        abort(f'Error trying to get data: {e}', 500)
        return jsonify([])

def get_floor_polygons_by_ids(building_id, floor_id, token):
    """Returns the polygons by buildingId and floorId"""
    headers = {'Authorization': token}
    api_url = BUILDINGS_URL + BUILDINGS_MODULE_API + str(building_id) + '/floors/'+ str(floor_id) + '/polygons'
    rv = requests.get(api_url, headers=headers)
    if rv.status_code == 200:
        return json.loads(rv.text)
    elif rv.status_code == 500:
        raise Exception("Cannot connect to the buildings module")
    return None
  
@app.route('/api/spaces/categories', methods=['GET'])
@token_required
def categories_spaces():
    """
        Show all categories and subcategories to be attached to a space
        ---
        produces:

            - "application/json"

        tags:

            - "spaces"

        responses:

            200:
                description: A list of all categories and their subcategories
            500:
                description: Internal Error

    """
    try:
        all_cat_dicts = [cat.to_dict() for cat in Category.query.all()]
        l=[]
        for cat in all_cat_dicts:
          d={}
          check=True
          if 'id' in cat:
            d['id']=cat['id']
            if 'name' in cat:
              d['name']=cat['name']
              if 'subcategories' in cat:
                d['subcategories']=[]
                for c in cat['subcategories']:
                  d1={}
                  if 'id' in c and 'name' in c:
                    d1['id']=c['id']
                    d1['name']=c['name']
                    
                    if 'spaces' in c and len(c['spaces'])>0:
                      d1['spaces']=[]
                      
                      for space in c['spaces']:
                        if 'id' in space:
                          sp = Space.query.filter_by(id=space['id']).first()
                          if sp is not None:
                            d1['spaces'].append({
                              'id': space['id'],
                              'name': sp.name,
                              'model_2d': sp.model_2d,
                              'model_3d': sp.model_3d,
                              'height': sp.height*m_px,
                              'width': sp.width*m_px
                              })
                          else: check=False

                        else: check=False
                    else: check=False
                    
                  else: check=False
                  d['subcategories'].append(d1)
                   
              else: check=False
            else: check=False
          else: check=False

          if check:
            l.append(d)

        
        return jsonify(l),200
    except Exception as e:
        abort(f'Error trying to get data: {e}', 500)

'''

def categories_spaces():
    """
        Show all categories and subcategories to be attached to a space
        ---
        produces:

            - "application/json"
        parameters:
          - in: "body"
            name: "body"
            required:
            - selected_floor
            - workspaces
        properties:
          selected_floor:
            type: object
            description: Data of the floor selected by the user.
            properties:
              id:
                type: integer
                description: Unique ID of each building floor.
              active:
                type: boolean
                description: indicate if this floor is active.
              wys_id:
                type: string
                description: Unique internal ID of each building floor.
              rent_value:
                type: number
                format: float
                description: Rent value of the floor
              m2:
                type: number
                format: float
                description: Square meter value of the floor.
              elevators_number:
                type: integer
                description: Numbers of elevators in the floor.
              image_link:
                type: string
                description: Link of the floor image.
              building_id:
                type: integer
                description: Unique ID of each building associated to this floor.
          workspaces:
            type: array
            items:
              type: object
              properties:
                id:
                  type: integer
                  description: Unique ID of each space.
                quantity:
                  type: integer
                  description: Quantity of the space
                name:
                  type: string
                  description: Name of the space
                height:
                  type: number
                  description: Height of the space
                width:
                  type: number
                  description: width of the space
                active:
                  type: boolean
                  description: indicate if this space is active
                regular:
                  type: boolean
                  description: indicate if this space is a regular space
                up_gap:
                  type: number
                  description: up padding
                down_gap:
                  type: number
                  description: down padding
                left_gap:
                  type: number
                  description: left padding
                right_gap:
                  type: number
                  description: right padding
                subcategory_id:
                  type: integer
                  description: subcategory Id
                points:
                  type: array
                  items:
                    type: object
                    properties:
                      x:
                        type: number
                        format: float
                        description: X coordinate of the vertex/point.
                      y:
                        type: number
                        format: float
                        description: Y coordinate of the vertex/point.
        tags:

            - "spaces"

        responses:

            200:
                description: A list of all categories and their subcategories
            500:
                description: Internal Error

    """
    req_params = {'selected_floor', 'workspaces'}
    #req_params = ["layout_workspaces", "layout_data"]
    for param in req_params:
      if param not in request.json.keys():
        abort(400, description=f"{param} isn't in body")
    floor = request.json['selected_floor']
    floor_params = {'id', 'wys_id','rent_value','m2','elevators_number','image_link','active','building_id'}
    if floor.keys() != floor_params:
      return "A floor data field is missing in the body", 400

    workspaces = request.json['workspaces']
    if len(workspaces) == 0:
        return "No spaces were entered in the body.", 400
    workspace_params = {'id','quantity','name','height','width','active','regular','up_gap','down_gap','left_gap',
                            'right_gap','subcategory_id','points'}
    categories =  [c.to_dict() for c in Category.query.all()]
    for category in categories:
      for subcategory in category['subcategories']:
        del subcategory['spaces']
    subcategories = categories

    for workspace in workspaces:
      if workspace.keys() != workspace_params:
        return "A space data field is missing in the body", 400
      found = False
      for category in subcategories:
        for subcategory in category['subcategories']:
          if subcategory['id'] == workspace['subcategory_id']:
            workspace['category_id'] = category['id']
            found = True
            break
        if found:
          break
      if not found:
        return "A Space subcategory doesn't exist", 404

      #project = get_project_by_id(project_id, token)
      #if project is None:
        #return "The project doesn't exist", 404
      token = request.headers.get('Authorization', None)
      floor_polygons = get_floor_polygons_by_ids(floor['building_id'], floor['id'], token)
      if floor_polygons is None or len(floor_polygons) == 0:
        return "The floor doesn't exist or not have a polygons.", 404
      floor['polygons'] = floor_polygons  
      layout_data = {'selected_floor': floor, 'workspaces': workspaces}
      workspaces_coords, floor_elements = transform_coords(layout_data, layout_workspaces)
    #layout_workspaces = request.json["layout_workspaces"]
    #layout_data = request.json["layout_data"]

    try:
        all_cat_dicts = [cat.to_dict() for cat in Category.query.all()]
        l=[]
        for cat in all_cat_dicts:
          d={}
          check=True
          if 'id' in cat:
            d['id']=cat['id']
            if 'name' in cat:
              d['name']=cat['name']
              if 'subcategories' in cat:
                d['subcategories']=[]
                for c in cat['subcategories']:
                  d1={}
                  if 'id' in c and 'name' in c:
                    d1['id']=c['id']
                    d1['name']=c['name']
                    
                    if 'spaces' in c and len(c['spaces'])>0:
                      d1['spaces']=[]
                      
                      for space in c['spaces']:
                        if 'id' in space:
                          sp = Space.query.filter_by(id=space['id']).first()
                          if sp is not None:
                            d1['spaces'].append({
                              'id': space['id'],
                              'name': sp.name,
                              'model_2d': sp.model_2d,
                              'model_3d': sp.model_3d,
                              'height': sp.height,
                              'width': sp.width
                              })
                          else: check=False

                        else: check=False
                    else: check=False
                    
                  else: check=False
                  d['subcategories'].append(d1)
                   
              else: check=False
            else: check=False
          else: check=False

          if check:
            l.append(d)

        
        return jsonify(l),200
    except Exception as e:
        abort(f'Error trying to get data: {e}', 500)
'''        

@app.route('/api/spaces/create', methods=['POST'])
@token_required
def new_space():
    """
        Save a new space
        ---
        consumes: 

            - "application/json"

        produces:

            - "application/json"

        tags:

            - "spaces"
            
        parameters:

            - in: "body"
              name: "body"
              required:
              - name
              - model_2d
              - model_3d
              - height
              - width
              - active
              - regular
              - up_gap
              - down_gap
              - left_gap
              - right_gap
              - subcategory_id
              properties:
                name:
                  type: string
                  description: name of the space
                model_2d:
                  type: string
                  description: Base64 file
                model_3d:
                  type: string
                  description: Base64 file
                height:
                  type: number
                  description: Height of the space
                width:
                  type: number
                  description: width of the space
                active:
                  type: boolean
                  description: indicate if this space is active
                regular:
                  type: boolean
                  description: indicate if this space is a regular space
                up_gap:
                  type: number
                  description: up padding
                down_gap:
                  type: number
                  description: down padding
                left_gap:
                  type: number
                  description: left padding
                right_gap:
                  type: number
                  description: right padding
                subcategory_id:
                  type: integer
                  description: subcategory Id

    """
    if request.is_json:
        try:
            res_space = request.get_json()
            space = Space(**res_space)
            db.session.add(space)
            db.session.commit()
            return space.serialize(), 201
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(f'Error saving data: {e}', 500)
        except Exception as e:
            db.session.rollback()
            abort(f'Unknown Error: {e}', 500)
    else:
        abort('Body isn\'t application/json', 400)


@app.route('/api/spaces/', methods=['GET'])
@token_required
def get_all_spaces():
    """
        Show all spaces
        ---
        produces:

            - "application/json"

        tags:

            - "spaces"

        responses:

            200:
                description: A list of all spaces
            500:
                description: Internal Error

    """
    try:
        spaces = Space.query.all()
        spaces_dict = [space.to_dict() for space in spaces]
        return jsonify(spaces_dict)
    except SQLAlchemyError as e:
        abort(f'Unknown Error f{e}', 500)
    except Exception as e:
        abort(f'Unknown Error f{e}', 500)


@app.route('/api/spaces/<space_id>', methods=['GET'])
@token_required
def get_space_by_id(space_id):
    """
        Get space By ID
        ---
        parameters:

            - in: path
              name: space_id
              type: integer
              description: Space ID

        tags:

            - "spaces"

        responses:

            200:
              description: Space Object
            404:
              description: Space Not Found
            500:
              description: "Database error"

    """
    try:
        space = Space.query.filter_by(id=space_id).first()
        if space is not None:
            if request.method == 'GET':
                return space.serialize(), 200

        return '{}', 404
    except Exception as exp:
        app.logger.error(f"Error in database: mesg ->{exp}")
        return exp, 500


@app.route('/api/spaces/<space_id>', methods = ['DELETE'])
@token_required
def deactivate_space_by_id(space_id):
    """
        Deactivate space By ID
        ---
        parameters:

            - in: path
              name: space_id
              type: integer
              description: Space ID

        tags:

            - "spaces"

        responses:

            200:
              description: Space Object or deactivated message
            404:
              description: Space Not Found
            500:
              description: "Database error"

    """
    try:
        space = Space.query.filter_by(id=space_id).first()
        if space is None:
            return '{}', 404
        space.active = False
        db.session.commit()
        return jsonify({'result': 'Space deactivated'}), 200
    except Exception as err:
        app.logger.error(f"Error in database: mesg ->{err}")
        return err, 500


@app.route('/api/spaces/<space_id>', methods=['PUT'])
@token_required
def update_space_by_id(space_id):
    """
        Update a space by ID
        ---
        consumes:

            - "application/json"

        produces:

            - "application/json"

        tags:

            - "spaces"
            
        parameters:

            - in: path
              name: space_id
              type: integer
              description: Space ID
              tags:
                - "spaces"
            - in: body
              name: body
              required:
              - name
              - model_2d
              - model_3d
              - height
              - width
              - active
              - regular
              - up_gap
              - down_gap
              - left_gap
              - right_gap
              - subcategory_id
              properties:
                name:
                  type: string
                  description: name of the space
                model_2d:
                  type: string
                  description: Base64 file
                model_3d:
                  type: string
                  description: Base64 file
                height:
                  type: number
                  description: Height of the space
                width:
                  type: number
                  description: width of the space
                active:
                  type: boolean
                  description: indicate if this space is active
                regular:
                  type: boolean
                  description: indicate if this space is a regular space
                up_gap:
                  type: number
                  description: up padding
                down_gap:
                  type: number
                  description: down padding
                left_gap:
                  type: number
                  description: left padding
                right_gap:
                  type: number
                  description: right padding
                subcategory_id:
                  type: integer
                  description: subcategory Id

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
        if space is None:
            return '{}', 404
        space.name = request.json['name'] if 'name' in request.json else space.name
        space.model_2d = request.json['model_2d'] if 'model_2d' in request.json else space.model_2d
        space.model_3d = request.json['model_3d'] if 'model_3d' in request.json else space.model_3d
        space.height = request.json['height'] if 'height' in request.json else space.height
        space.width = request.json['width'] if 'width' in request.json else space.width
        space.active = request.json['active'] if 'active' in request.json else space.active
        space.regular = request.json['regular'] if 'regular' in request.json else space.regular
        space.up_gap = request.json['up_gap'] if 'up_gap' in request.json else space.up_gap
        space.down_gap = request.json['down_gap'] if 'down_gap' in request.json else space.down_gap
        space.left_gap = request.json['left_gap'] if 'left_gap' in request.json else space.left_gap
        space.right_gap = request.json['right_gap'] if 'right_gap' in request.json else space.right_gap
        space.subcategory_id = request.json['subcategory_id'] if 'subcategory_id' in request.json else space.subcategory_id

        db.session.commit()

        space_updated = Space.query.filter_by(id=space_id).first()

        return space_updated.serialize(), 200

    except Exception as err:
        app.logger.error(f"Error in database: mesg ->{err}")
        return err, 500

@app.route('/api/spaces/<space_id>/points', methods=['POST'])
@token_required
def save_space_points_by_id(space_id):
    """
        Save points of irregular space By ID
        ---
        parameters:

            - in: path
              name: space_id
              type: integer
              description: Irregular Space ID
            - in: body
              name: body
              required: true
              schema:
                type: array
                items:
                  type: object
                  properties:
                    x:
                      type: number
                      format: float
                      description: X coordinate of the vertex/point.
                    y:
                      type: number
                      format: float
                      description: Y coordinate of the vertex/point.

        tags:

            - "spaces/points"

        responses:

            200:
              description: Saved Points list.
            400:
              description: Body isn't application/json, the space isn't irregular or empty body list
            404:
              description: Space Not Found
            500:
              description: Internal server error or Database error

    """
    try:
      if request.is_json:
        space = Space.query.get(space_id)
        if space is None:
          return 'Error: Space Not Found', 404
        elif space.regular:
          return 'Bad Request: The sent ID corresponds to a regular space', 400
        elif len(request.json) == 0:
          return 'Bad Request: The entered list of points in the body is empty', 400
        elif any({'x','y'} != data.keys() for data in request.json):
          return "Bad Request: A required field is missing in the body", 400
        
        if len(space.points) > 0:
          for point in space.points:
            p = Point.query.get(point.id)
            db.session.delete(p)
            db.session.commit()

        for i in range(len(request.json)):
          point = Point(**request.json[i])
          point.order = i
          space.points.append(point)

        db.session.commit()

        points =  [p.to_dict() for p in space.points]

        return jsonify(points), 201
      else:
        return 'Body isn\'t application/json', 400
    except SQLAlchemyError as e:
      return f'Error getting data: {e}', 500
    except Exception as exp:
      app.logger.error(f"Error in server: mesg ->{exp}")
      return exp, 500

@app.route('/api/spaces/subcategories', methods=['GET'])
@token_required
def get_all_subcategories():
    """
        Get all subcategories with their categories (without their associated spaces).
        ---
        tags:

            - "spaces/subcategories"

        responses:

            200:
              description: List of categories + subcategories. 
            500:
              description: "Database error"

    """
    try:
        categories =  [c.to_dict() for c in Category.query.all()]
        for category in categories:
          for subcategory in category['subcategories']:
            del subcategory['spaces']

        return jsonify(categories), 200
    except SQLAlchemyError as e:
        abort(f'Error getting data: {e}', 500)

@app.route('/api/spaces/subcategories', methods=['PUT'])
@token_required
def update_subcategories():
    """
        Update subcategories values (for now, unit area only)
        ---
        produces:

            - "application/json"

        tags:

            - "spaces/subcategories"

        parameters:

            - in: "body"
              name: "body"
              description: "List of subcategories values to be updated."
              schema:
                type: array
                items:
                  type: object
                  properties:
                    id: 
                      type: integer
                    unit_area:
                      type: number

        responses:

            200:
              description: List of updated subcategories. 
            400:
              description: Body isn't application/json or empty body data
            500:
              description: "Database error"

    """
    if request.is_json:
        if len(request.json) > 0:
            try:
                db.session.bulk_update_mappings(Subcategory, request.json)
                db.session.commit()
                ids = [s['id'] for s in request.json]
                updated_subcategories =  [s.to_dict() for s in db.session.query(Subcategory).filter(Subcategory.id.in_(ids)).all()]
                for subcategory in updated_subcategories:
                  del subcategory['spaces']

                return jsonify(updated_subcategories), 200
            except SQLAlchemyError as e:
                abort(f'Database error: {e}', 500)
        else:
            abort('Body data required', 400)
    else:
        abort('Body isn\'t application/json', 400)

if __name__ == '__main__':
    app.run(host = APP_HOST, port = APP_PORT, debug = True)
