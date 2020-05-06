from cvapp.app import app, db
from cvapp.models import User, Skill, UserSkillAssociations
from flask import jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import DetachedInstanceError


@app.route("/api/user", methods=['GET'])
def get_all_users():
    return jsonify([user.serialize for user in User.query.all()])


@app.route("/api/user", methods=['POST'])
def create_user():
    if not request.json:
        return "Missing body", 400
    if not all(key in request.json for key in User.required_keys()):
        return f"Body must contain required properties: {User.required_keys()}", 400

    try:
        skills = request.json.pop("skills")
        user = User(**request.json)
        skill_associations = []
        for s in skills:
            if not all(key in s for key in UserSkillAssociations.required_keys()):
                return f"Property 'skill' must contain required keys: {UserSkillAssociations.required_keys()}", 400
            skill = Skill.query.filter_by(name=s["name"]).first()
            if not skill:
                return f"Given skill '{s['name']}' does not exist", 400
            skill_associations.append(UserSkillAssociations(user_id=user.id, skill=skill, level=s["level"]))
        user.skill_associations = skill_associations

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
        user = User.query.get_or_404(user_id)
        user.skill_associations = []
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.serialize)
    except IntegrityError or DetachedInstanceError:
        db.session.rollback()
        return f"User with id={user_id} was not found", 404


@app.route("/api/skill", methods=['POST'])
def create_skill():
    if not request.json:
        return "Missing body", 400
    if not "name" in request.json:
        return f"Body does not contain required property: 'name'", 400

    try:
        skill = Skill(**request.json)
        db.session.add(skill)
        db.session.commit()
        return jsonify(skill.serialize), 201
    except IntegrityError:
        db.session.rollback()
        return "This skill already exist", 400


@app.route("/api/skill", methods=['GET'])
def get_all_skills():
    return jsonify([skill.serialize for skill in Skill.query.all()])
