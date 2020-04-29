from cvapp.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    cv_url = db.Column(db.String())
    # skill # todo

    def __repr__(self):
        return f"User({self.id}, '{self.first_name}', '{self.last_name}', '{self.cv_url}')"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "cv_url": self.cv_url
        }

    @staticmethod
    def required_properties():
        return "first_name", "last_name", "cv_url"


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __repr__(self):
        return f"Skill({self.id}, '{self.name}')"


class UserSkillAssociations(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship("User", foreign_keys=[user_id])
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False)
    skill = db.relationship("Skill", foreign_keys=[skill_id])
    level = db.Column(db.Integer)

    __table_args__ = (
        db.PrimaryKeyConstraint(user_id, skill_id),
    )
