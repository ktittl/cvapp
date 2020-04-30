from cvapp.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    cv_url = db.Column(db.String())
    skill_associations = db.relationship("UserSkillAssociations", backref="user", lazy=True,
                                         cascade="all, delete-orphan")

    def __repr__(self):
        return f"User({self.id}, '{self.first_name}', '{self.last_name}', '{self.cv_url}', '{self.skill_associations}')"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "cv_url": self.cv_url,
            "skills": [s.serialize for s in self.skill_associations]
        }

    @staticmethod
    def required_keys():
        return "first_name", "last_name", "cv_url", "skills"


class Skill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return f"Skill({self.id}, '{self.name}')"

    @property
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name
        }


class UserSkillAssociations(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), nullable=False, primary_key=True)
    skill = db.relationship("Skill", foreign_keys=[skill_id])
    level = db.Column(db.Integer)

    def __repr__(self):
        return f"Skill({self.skill.name}, '{self.level}')"

    @property
    def serialize(self):
        return {
            "name": self.skill.name,
            "level": self.level
        }

    @staticmethod
    def required_keys():
        return "name", "level"
