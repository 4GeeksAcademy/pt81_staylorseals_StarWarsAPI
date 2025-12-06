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
from models import db, User, People, Planets
# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace(
        "postgres://", "postgresql://")
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


@app.route('/people', methods=["GET", "POST"])
def handle_people():
    if request.method == "POST":
        name = request.json["name"]
        description = request.json["description"]
        new_person = People(
            name=name,
            description=description
        )

        return jsonify(new_person.serialize()), 201

    people = People.query.all()
    people_dictionaries = []
    for person in people:
        people_dictionaries.append(
            person.serialize()
        )

    return jsonify(people_dictionaries), 200


@app.route('/people/<int:people_id>', methods=["GET"])
def get_person(people_id):
    person = People.query.get(people_id)
    if person is None:
        return jsonify({
            "msg": "Character not found"
        }), 404
    return jsonify(person.serialize()), 200


@app.route('/favorite/people/<int:people_id>', methods=["POST"])
def add_favorite_person(people_id):
    user_id = request.json.get("user_id")

    # 1. get the user
    user = User.query.get(user_id)
    if not user:
        return {"error": "User not found"}, 404

    # 2. get the person
    person = People.query.get(people_id)
    if not person:
        return {"error": "Person not found"}, 404

    # 3. add person to user's favorites using relationship
    user.favorites.append(person)

    # 4. commit
    db.session.commit()

    return {"message": "Favorite added successfully"}


@app.route('/users', methods=["GET", "POST"])
def handle_users():
    if request.method == "POST":
        email = request.json["email"]
        new_user = User(
            email=email,
        )

        return jsonify(new_user.serialize()), 201

    users = User.query.all()
    users_dictionaries = []
    for user in users:
        users_dictionaries.append(
            user.serialize()
        )

    return jsonify(users_dictionaries), 200

    # this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
