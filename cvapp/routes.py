from cvapp.app import app, db
from cvapp.models import User
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError


@app.route("/api/user", methods=['GET'])
def get_all_users():
    return jsonify([user.serialize for user in User.query.all()])


@app.route("/api/user", methods=['POST'])
def create_user():
    if not request.json:
        return "Missing body", 400
    if not all(key in request.json for key in User.required_properties()):
        return f"Body does not contain all required properties: {User.required_properties()}", 400

    try:
        user = User(**request.json)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.serialize), 201
    except IntegrityError:
        db.session.rollback()
        return "This user already exist", 400


@app.route("/api/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize)


@app.route("/api/user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    try:
        user = User.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return f"User with id={user_id} was not found", 404

    return jsonify(user.serialize)
