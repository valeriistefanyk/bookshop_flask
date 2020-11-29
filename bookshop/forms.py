from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Length, email, required, EqualTo
from bookshop.models import User


class BookForm(FlaskForm):
    title = StringField('Назва', [Length(min=4, max=60)])
    description = StringField('Опис')

class SignupForm(FlaskForm):
    email = StringField('Email', validators=[email(), required()])
    password = PasswordField('Пароль', validators=[required(), Length(min=6), EqualTo('confirm', message='Паролі повинні збігатися')])
    confirm = PasswordField('Підтверження пароля', validators=[required()])

    def validate(self):
        check_validate = super().validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append('Акаунт з цим email вже існує')
            return False
        return True
