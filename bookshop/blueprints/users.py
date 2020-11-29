from flask import Blueprint

users = Blueprint('users', __name__)

@users.route('/register')
def register():
    return "<h1>Register</h1>"