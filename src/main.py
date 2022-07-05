"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Planets, Characters, FavsCharacters, FavsPlanets
import json
#from models import Person



app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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


# GET USERS

@app.route('/user', methods=['GET'])
def handle_user():

    users = User.query.all() #le pido info a la tabla User
    userList = list(map(lambda obj: obj.serialize(),users))
    response_body = {
        "results": userList
    }

    return jsonify(response_body), 200


# PLANETS

# CREATE PLANET LIST IN DB

# Fetch
url = 'https://swapi.dev/api/planets'
response = requests.get(url)
result = json.loads(response.text)
planetList = result["results"]



# GET PLANETS 

@app.route('/planets', methods=['GET'])
def handle_planets():


    for planet in planetList:
        newPlanet = Planets(name= planet["name"], population= planet["population"], terrain=planet["terrain"], climate=planet["climate"], orbitalPeriod= planet["orbital_period"], diameter=planet["diameter"])
        db.session.add(newPlanet)
        db.session.commit()

   
    planeta = Planets.query.all() #le pido info a la tabla User
    planetsList = list(map(lambda obj: obj.serialize(), planeta)) #mapeo el array para serializarlo
    print(planetsList)

    response_body = {
        "results": planetsList
    }

    return jsonify(response_body)

# GET CHARACTERS

@app.route('/characters', methods=['GET'])
def handle_characters():

   
    characters = Characters.query.all() #le pido info a la tabla User
    characterList = list(map(lambda obj: obj.serialize(),characters))

    print(characters)

    response_body = {
        "results": characterList
    }

    return jsonify(response_body)


#  GET USER FAVORITES CHARACTERS

@app.route('/user/<int:position>/CharactersFavorites', methods=['GET'])
def handle_favCharacter(position):
    fav = FavsCharacters.query.all() #le pido info a la tabla User
    userList = list(map(lambda obj: obj.serialize(),fav))

    result =[]
    for obj in userList:
        if obj["person_id"]== position:
            result.append(obj)

    response_body = {
        "results": result
    }

    return jsonify(response_body), 200


#  GET USER FAVORITES PLANETS

@app.route('/user/<int:position>/PlanetsFavorites', methods=['GET'])
def handle_favPlanet(position):

    fav = FavsPlanets.query.all() #le pido info a la tabla User
    userList = list(map(lambda obj: obj.serialize(),fav))

    result =[]
    for obj in userList:
        # print(obj)
        if obj["person_id"]== position:
            result.append(obj)

    response_body = {
        "results": result
    }

    return jsonify(response_body), 200


# GET USER  ALL FAVORITES

@app.route('/user/<int:position>/Favorites', methods=['GET'])
def handle_favs(position):

    favList=[]
    planetas = FavsPlanets.query.all() #le pido info a la tabla User
    characters = FavsCharacters.query.all() #le pido info a la tabla User
    planet = list(map(lambda obj: obj.serialize(),planetas))
    character = list(map(lambda obj: obj.serialize(),characters))
    # print(planet)
    for plan in planet:
        if plan["person_id"]==position:
            favList.append(plan)
    
    for charac in character:
        # print(charac)
        if charac["person_id"]==position:
            favList.append(charac)

    response_body = {
        "results": favList
    }

    return jsonify(response_body), 200


# POST USER 

@app.route('/user', methods=['POST'])
def add_new_user():

    body = json.loads(request.data)
    
    user = User(name= body["name"], email=body["email"], password=body["password"])
    db.session.add(user)
    db.session.commit()

    response_body = {
        "msg": "user created"
    }

    return jsonify(response_body), 200


# POST FAVORITE CHARACTER

@app.route('/user/CharactersFavorites/<int:id_character>/', methods=['POST'])
def add_new_favCharacter(id_character):

    body = json.loads(request.data)
    favorite = FavsCharacters(person_id= body["person_id"], character_id = body['id_character'])
    db.session.add(favorite)
    db.session.commit()

    response_body = {
        "msg": "character created"
    }

    return jsonify(response_body), 200


# POST FAVORITE PLANET

@app.route('/user/PlanetsFavorites/<int:id_planet>/', methods=['POST'])
def add_new_favPlanet(id_planet):

    body = json.loads(request.data)
    favorite = FavsPlanets(person_id= body["person_id"], planets_id = body['id_planet'])
    db.session.add(favorite)
    db.session.commit()

    response_body = {
        "msg": "planet created"
    }

    return jsonify(response_body), 200


# DELETE USER


@app.route('/user/<int:position>', methods=['DELETE'])
def delete_user(position):
    usuario = User.query.filter_by(id= position).first()
    # print(usuario)
    db.session.delete(usuario)
    db.session.commit()

    response_body = {
        "msg": "user deleted"
    }

    return jsonify(response_body), 200


# DELETE FAVORITE PLANET

@app.route('/user/<int:id_user>/PlanetsFavorites/<int:id_planet>/', methods=['DELETE'])
def delete_PlanetsFavorites(id_user,id_planet):
    # body = json.loads(request.data)
    # print(body)
    planeta = FavsPlanets.query.filter_by(planets_id= id_planet, person_id=id_user).first()
    print(planeta)
    db.session.delete(planeta)
    db.session.commit()

    response_body = {
        "msg": "user deleted"
    }

    return jsonify(response_body), 200

# DELETE FAVORITE CHARACTER

@app.route('/user/<int:id_user>/CharactersFavorites/<int:id_character>/', methods=['DELETE'])
def delete_CharactersFavorites(id_user,id_character):
    # body = json.loads(request.data)
    # print(body)
    character = FavsCharacters.query.filter_by(person_id= id_user, character_id= id_character).first()
    db.session.delete(character)
    db.session.commit()

    response_body = {
        "msg": "user deleted"
    }

    return jsonify(response_body), 200

















# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
