from cvapp import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return f"User({self.id}, '{self.username}')"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'username': self.username
        }