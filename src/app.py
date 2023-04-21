"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route ("/people", methods="GET")
def list_all_people():
    pass

@app.route ("people/<int:people_id>", methods="GET")
def list_one_people(people_id):
    pass

@app.route ("/planets", methods="GET")
def list_all_people():
    pass

app.route ("planets/<int:planets_id>", methods="GET")
def list_one_people(planets_id):
    pass

#end points para poder tener usuarios en nuestro blog

@app.route("/users", methods="GET")
def list_all_users():
    pass

@app.route("/users/favorites", methods="GET")
def favorites_per_user():
    pass

@app.route("/users/favorites<int:planet_id>", methods="POST")
def add_favorite_planet(id):
    pass

@app.route("/users/favorites<int:people_id>", methods="POST")
def add_people(id):
    pass

@app.route("/users/favorites<int:planet_id>", methods="DELETE")
def delete_favorite_planet(id):
    pass

@app.route("/users/favorites<int:people_id>", methods="POST")
def delete_people(id):
    pass

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)