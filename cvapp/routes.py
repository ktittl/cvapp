from cvapp import app
from cvapp import db
from cvapp.models import User
from flask import jsonify, request


@app.route("/")
def home():
    return "<h1>CV database app</h1>"


@app.route("/api/user", methods=['GET'])
def get_all_users():
    return jsonify([user.serialize for user in User.query.all()])


@app.route("/api/user", methods=['POST'])
def create_user():
    if not request.json or not "username" in request.json:
        return "Invalid body", 400
    user = User(username=request.json["username"])
    db.session.add(user)
    db.session.commit()
    id = user.id
    user = User.query.get(id)
    return jsonify(user.serialize), 201


@app.route("/api/user/<int:user_id>", methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.serialize)


@app.route("/api/user/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "User deleted"
