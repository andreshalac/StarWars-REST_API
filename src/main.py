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
from models import db, User, Planets, Characters
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

# listaPlanets = [{"eh":"o"}]

# db.session.add(listaPlanets)
# db.session.commit()


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_user():

    users = User.query.all() #le pido info a la tabla User
    userList = list(map(lambda obj: obj.serialize(),users))
    user = User(name= body["name"], email=body["email"], password=body["password"])
    response_body = {
        "results": userList
    }

    return jsonify(response_body), 200

planets = [{"id":1, "name":"a", "population":"b", "terrain":"h", "climate":"b","orbitalPeriod":"ij","rotationPeriod":"ij", "diameter":"ij","favoritos":"huhu"}]





@app.route('/planets', methods=['GET'])
def handle_planets():


    for planet in planets:
        newPlanet = Planets(name= planet["name"], population= planet["population"], terrain=planet["terrain"], climate=planet["climate"], orbitalPeriod= planet["orbitalPeriod"], diameter=planet["diameter"], favoritos = planet["favoritos"])
        db.session.add(newPlanet)
        db.session.commit()
   
    planeta = Planets.query.all() #le pido info a la tabla User
    # planetsList = list(map(lambda obj: obj.serialize(),planeta))
    print(planeta)

    response_body = {
        "results": "ok"
    }


    return jsonify(response_body), 200

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

@app.route('/user/<int:position>', methods=['DELETE'])
def delete_todo(position):

    def delete(todo):
        user= []

    return jsonify(user)
    # def delete(todo):

    #     if todos.index(todo) != position:
    #         return todos[todos.index(todo)]

    # newTodos = list(filter(delete, todos))
    # newTodos = jsonify(newTodos)
    
    # print(newTodos)

    # return newTodos

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
