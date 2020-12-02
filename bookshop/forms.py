from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import StringField, PasswordField
from wtforms.validators import (Length, email, EqualTo, DataRequired)

from bookshop.models import User


class BookForm(FlaskForm):
    title = StringField('Назва', [Length(min=4, max=60)])
    description = StringField('Опис')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[email(), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6), EqualTo('confirm', message='Паролі повинні збігатися')])
    confirm = PasswordField('Підтверження пароля', validators=[DataRequired()])

    def validate(self):
        check_validate = super().validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Акаунт з цим email вже існує')
            return False
        return True

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[email(), DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])

    def validate(self):
        check_validate = super().validate()
        if not check_validate:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if not user and not check_password_hash(
                            user.password, 
                            self.password.data):
            self.email.errors.append('Неправильний email або пароль')
            return False
        return True
