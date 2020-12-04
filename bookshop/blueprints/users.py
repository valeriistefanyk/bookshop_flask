from flask import (Blueprint, redirect, url_for, render_template, 
                flash, session, request)
from flask_login import (login_user, current_user, login_required,
                logout_user)
from flask_babel import _

from bookshop.forms import SignupForm
from bookshop.models import User
from bookshop.extenstions import db, login_manager
from bookshop.forms import SignupForm, LoginForm


users = Blueprint('users', __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    session['after_login'] = request.url
    flash(_('You need to login'), 'warning')
    return redirect(url_for('users.login'))


@users.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(_('You cannot register an account because the account is already registered. '
                'If you want to register a new user, you must logout this account'), 'warning')
        return redirect('/')
    form = SignupForm()
    if form.validate_on_submit():
        user = User.create(form.email.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(_('Registered success'), 'success')
        return redirect(url_for('books.index'))
    return render_template('users/register.html', form=form)

@users.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(_('You are already logged in'), 'warning')
        return redirect(url_for('books.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).one()
        login_user(user)
        flash(_('Logged in successfully'), 'success')
        return redirect(session.get('after_login') or 
                            url_for('books.index'))
    return render_template('users/login.html', form=form)

@users.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect('/')
