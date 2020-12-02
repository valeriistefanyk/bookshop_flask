from werkzeug.security import generate_password_hash
from sqlalchemy.orm import validates
from flask_login import UserMixin

from bookshop.extenstions import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=True)

    @validates('title')
    def validate_title(self, key, title):
        if len(title.strip()) <= 2:
            raise ValueError('Needs to have a real title')
        return title

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    @classmethod
    def create(cls, email, password):
        """
        Usage: User.create('test@example.com', 'example')
        """
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)
