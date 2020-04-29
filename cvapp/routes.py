from cvapp import app
from cvapp import db
from cvapp.models import User, user_schema, users_schema
from flask import jsonify, request


@app.route("/api/user", methods=['GET'])
def get_all_users():
    result = users_schema.dump(User.query.all())
    return jsonify(result)


@app.route("/api/user", methods=['POST'])
def create_user():
    if not request.json or not "first_name" in request.json:
        return "Invalid body", 400
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    user = User(first_name=first_name, last_name=last_name)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201


@app.route("/api/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.jsonify(user)


@app.route("/api/user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return user_schema.jsonify(user)
