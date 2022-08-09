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
from models import db, User, People, Planet
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
# Listar todos los usuarios del blog
@app.route('/users', methods=['GET'])
def get_all_Users():
    try:
        response = [x.serialize() for x in User.query.all()]
        return jsonify(response), 200
    except:
        return "invalid Method ", 401
# Elimina un planet favorito con el id = planet_id`.
@app.route('/planetfavorites/<int:planet_id>',methods=['DELETE'])
def delete_planetfavorites(planet_id):

    users = request.json.get("User")
    userObj = User.query.filter_by( id = users["id"]).first()
    planetObj = Planet.query.filter_by(id = planet_id).first()
    userObj.planetfavourites.remove(planetObj)
    db.session.commit()
    return jsonify("Planet deleted",200)

# Elimina un people favorito con el id = people_id`.
@app.route('/peoplefavorites/<int:people_id>',methods=['DELETE'])
def delete_peoplefavorites(people_id):

    users = request.json.get("User")
    userObj = User.query.filter_by( id = users["id"]).first()
    peopleObj = People.query.filter_by(id = people_id).first()
    userObj.peoplefavourites.remove(peopleObj)
    db.session.commit()
    return jsonify("People deleted",200)


#  Añade un nuevo planet favorito al usuario
@app.route('/planetfavorites/<int:planet_id>', methods=['POST'])
def post_PlanetFavorites(planet_id):

    users = request.json.get("User")
    userObj = User.query.filter_by( id = users["id"]).first()
    planetObj = Planet.query.filter_by(id = planet_id).first()

    if not  userObj or not planetObj:
        raise APIException("User or planet not found",404)

    elif planetObj in userObj.planetfavourites:

        raise APIException("Planet on favorites",400)

    else:
        userObj.planetfavourites.append(planetObj)
        db.session.commit()

        return jsonify("Planet add",200)

#  Añade un nuevo people favorito al usuario
@app.route('/peoplefavorites/<int:people_id>', methods=['POST'])
def post_PeopleFavorites(people_id):

    users = request.json.get("User")
    userObj = User.query.filter_by( id = users["id"]).first()
    peopleObj = People.query.filter_by(id = people_id).first()

    if not  userObj or not peopleObj:
        raise APIException("User or people not found",404)

    elif peopleObj in userObj.peoplefavourites:

        raise APIException("people on favorites",400)

    else:
        userObj.peoplefavourites.append(peopleObj)
        db.session.commit()

        return jsonify("People add",200)

#  Listar todos los registros de people en la base de datos
@app.route('/people', methods=['GET'])
def get_all_people():
    try:
        response = [x.serialize() for x in People.query.all()]
        return jsonify(response),200
    except:
        return "invalid Method ", 400
# Listar la información de una sola people
@app.route('/people/<int:id>', methods=['GET'])
def get_one_people(id):
    try:
        response = People.query.get(id)
        return jsonify(response.serialize()),200
    except:
        return "invalid Method ", 400
#  Listar todos los registros de planet en la base de datos
@app.route('/planet', methods=['GET'])
def get_all_planet():
    try:
        response = [x.serialize() for x in Planet.query.all()]
        return jsonify(response),200
    except:
        return "invalid Method ", 400
# Listar la información de un solo planet
@app.route('/planet/<int:id>', methods=['GET'])
def get_one_planet(id):
    
    response = Planet.query.get(id)
    return jsonify(response.serialize()),200
    
@app.route('/favorites',methods=['GET'])        
def get_all_favourites():
    
    user = request.json.get("User")
    userObj = User.query.filter_by( id = user["id"]).first()
    favorites = [favorite.serialize() for favorite in userObj.planetfavourites + userObj.peoplefavourites]
    return jsonify(favorites), 200

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
