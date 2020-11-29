from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Length


class BookForm(FlaskForm):
    title = StringField('Назва', [Length(min=4, max=60)])
    description = StringField('Опис')