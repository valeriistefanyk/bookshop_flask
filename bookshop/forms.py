from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l, _
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import (Length, email, EqualTo, DataRequired)

from bookshop.models import User


class BookForm(FlaskForm):
    title = StringField(_l('Title'), [Length(min=4, max=60)])
    description = StringField(_l('Description'))

class SignupForm(FlaskForm):
    email = StringField(_l('Email'), validators=[email(), DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=6), EqualTo('confirm', message=_l('Passwords must match'))])
    confirm = PasswordField(_l('Password confirm'), validators=[DataRequired()])
    store_name = StringField(_l('Store Name'), validators=[DataRequired(), Length(min=4)])

    def validate(self):
        check_validate = super().validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(_('An account with this email already exists'))
            return False
        return True

class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[email(), DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])

    def validate(self):
        check_validate = super().validate()
        if not check_validate:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user or not check_password_hash(
                            user.password, 
                            self.password.data):
            self.email.errors.append(_('Invalid email or password'))
            return False
        return True
