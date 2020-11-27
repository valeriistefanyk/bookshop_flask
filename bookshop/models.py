from sqlalchemy.orm import validates
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