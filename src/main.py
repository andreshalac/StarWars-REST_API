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

user=[]

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

    users = jsonify(user)
    return users
    # response_body = {
    #     "msg": "Hello, this is your GET /user response "
    # }

    # return jsonify(response_body), 200

@app.route('/user', methods=['POST'])
def add_new_user():

    request_body =  json.loads(request.data)
    user.append(request_body)
    user_json = jsonify(user)

    return user_json

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
