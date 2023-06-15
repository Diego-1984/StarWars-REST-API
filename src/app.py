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
from models import db, User, People, Favorite, Planet
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

@app.route ("/people", methods=["GET"])
def list_all_people():
    characters = People.query.all()
    response_people = [people.serialize() for people in characters]
    response_body ={
        "msg": "Esta es la lista de personajes"
    }
    return jsonify(response_people), 200

@app.route ("/user/<int:user_id>", methods = ["GET"])
def get_one_user(user_id):
    user = User.query.get(user_id)
    user = user.serialize()
    return jsonify(user), 200
    
@app.route ("/character/<int:people_id>", methods = ["GET"])
def get_one_character(people_id):
    character = Character.query.get(people_id)
    character = character.serialize()
    return jsonify(character), 200

@app.route ("/planet", methods = ["GET"])
def list_all_planets():
    planets = Planet.query.all()
    response_planets = [planet.serialize() for planet in planets]
    response_body ={
        "msg":"Esta es la lista de planetas", 
        "planets": response_planets
    }
    return jsonify(response_body), 200

@app.route ("/planet/<int:planet_id>", methods = ["GET"])
def get_one_plantet(planet_id):
    planet =  Planet.query.get(planet_id)
    planet = planet.serialize()
    return jsonify(planet), 200


@app.route("/user", methods= ["GET"])
def list_all_users():
    users = User.query.all()
    response_user = [user.serialize() for user in users]
    response_body ={
        "msg":"Esta es la lista de usuarios",
        "users": response_user
    }
    return jsonify(response_body), 200

@app.route("/<int:user_id>/favorites", methods = ["GET"])
def favorites_per_user(user_id):
    favorites = Favorite.query.filter_by(user_id = user_id).all()
    favorite_user = [favorite.serialize() for favorite in favorites]
    return jsonify(favorite_user), 200
    

@app.route("/<int:user_id>/favorite/<int:id>", methods = ["POST"])
def add_favorite(user_id, id):
    favorite = Favorite (user_id = user_id, basic_data_id = id)
    db.session.add(favorite)
    db.session.commit()
    response_body ={
        "msg":"Favorito agregado"
    }
    return jsonify(response_body), 200
    

@app.route("/<int:user_id>/favorite/<int:id>", methods = ["DELETE"])
def delete_favorite(user_id, id):
    favorite_deleted = Favorite.query.filter_by(user_id = user_id, basic_data_id = id).first()
    db.session.delete(favorite_deleted)
    db.session.commit
    response_body = {
        "msg":"Favorito eliminado"
    }
    return jsonify(response_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
