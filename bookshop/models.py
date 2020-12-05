from werkzeug.security import generate_password_hash
from sqlalchemy.orm import validates
from flask_login import UserMixin
from flask_babel import _

from bookshop.extenstions import db


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(120), nullable=True)
    price_kopecks = db.Column(db.Integer)
    picture_url = db.Column(db.Text)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    store_id = db.Column(db.Integer, db.ForeignKey('store.id'))

    creator = db.relationship('User', uselist=False, back_populates='books')
    store = db.relationship('Store', uselist=False, back_populates='books')

    @validates('title')
    def validate_title(self, key, title):
        if len(title.strip()) <= 2:
            raise ValueError(_('Needs to have a real title'))
        return title

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

    store = db.relationship('Store', uselist=False, back_populates='user')
    books = db.relationship('Book', back_populates='creator')

    @classmethod
    def create(cls, email, password):
        """
        Usage: User.create('test@example.com', 'example')
        """
        hashed_password = generate_password_hash(password)
        return User(email=email.lower().strip(), password=hashed_password)

class Store(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    user = db.relationship('User', uselist=False, back_populates='store')
    books = db.relationship('Book', back_populates='store')

    @validates('name')
    def validate_name(self, key, name):
        if len(name.strip()) <= 3:
            raise ValueError(_('Needs to have a real store name'))
        return name
