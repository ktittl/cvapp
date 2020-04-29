from cvapp import db, ma


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    cv_url = db.Column(db.String())

    def __repr__(self):
        return f"User({self.id}, '{self.first_name}', '{self.last_name}', '{self.cv_url}')"


class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "cv_url")


user_schema = UserSchema()
users_schema = UserSchema(many=True)


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
