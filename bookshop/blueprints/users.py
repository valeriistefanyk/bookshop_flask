from flask import Blueprint, redirect, url_for, render_template
from bookshop.forms import SignupForm
from bookshop.models import User
from bookshop.extenstions import db

users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    form = SignupForm()
    if form.validate_on_submit():
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('books.index'))
    return render_template('users/register.html', form=form)