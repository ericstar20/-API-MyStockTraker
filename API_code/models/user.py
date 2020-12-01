# Since the class User is not related to the resources. We seperate it from the resources.user.py
from db import db

class UserModel(db.Model):

    # SQLAlchemy
    __tablename__ = 'users'
    # Users' Columns info
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    # searching user info inside the db by username
    @classmethod # use current class(User) to the function
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    # searching user info inside the db by id
    @classmethod # use current class(User) to the function
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
