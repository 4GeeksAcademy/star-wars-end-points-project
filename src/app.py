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
from models import db, User, Planet, Character, UserPlanetFavorite, UserCharacterFavorite, meth
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

#---------------------------------------------------------------------------------------------------------------------------------------


#[GET] /users/favorites Get all the favorites
#[POST] /favorite/planet/<int:planet_id> Add a new favorite planet
#[POST] /favorite/people/<int: people_id> Add a new favorite person
#[DELETE] / favorite/planet/<int:planet_id> Delete a favorite planet
#[DELETE] / favorite/people/<int:people_id> Delete a favorite person

#add (POST), update (PUT), and delete (DELETE) planets and people

#model_type = User if type = “users” else Planet if type = “planets” else Character if type = “people” else UserPlanetFavorite if type = “favorite_planes” else  UserCharacterFavorite if type = “favorite_people” else False


#[GET] /users/favorites

#[POST]/favorite/<string: fav>/<string: obj_id> + data(user id)
#[DELETE]/favorite/<string: fav>/<string: obj_id> + data(user id)

#Get all: [GET] /<string: type>/

#Add: [POST] /<string: type>/<string: obj_id> + data
#Update: [PUT] /<string: type>/<string: obj_id> + data
#Delete: [DELETE] /<string: type>/<string: obj_id>
#Get one: [GET] /<string: type>/<string: obj_id>


@app.route(" /<string: type>/<string: obj_id> ", methods=["GET", "POST", "DELETE", "PUT"])
def generic_actions():
    data = request.get_json() or {}
    if obj_id is not "none": data["id"] = obj_id
#i don't know if i should do the if here or in models: <-------------------------------------------------------------------------<<<<<<<<<
    if request.method == "GET":
        if data["id"]:
            return meth.get_all(type)
        meth.get_one(type, )

    elif request.method == "POST":
        data = request.get_json()
        return jsonify({"message": "Received POST request", "data": data})

    #elif request.method == "DELETE":

    #elif request.method == "PUT":



#---------------------------------------------------------------------------------------------------------------------------------------

@app.route('/users')
def list_users():
    users = User.query.all()
    return '\n'.join([user.username for user in users])


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
