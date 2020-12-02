import pytest
from flask import url_for

from bookshop.models import User
from bookshop.extenstions import db


EXAMPLE_EMAIL = 'test@example.com'
EXAMPLE_PASSWORD = 'test123'

VALID_REGISTER_PARAMS = {
    'email': EXAMPLE_EMAIL,
    'password': EXAMPLE_PASSWORD,
    'confirm': EXAMPLE_PASSWORD
}

def create_user(email=EXAMPLE_EMAIL, password=EXAMPLE_PASSWORD):
    user = User.create(email, password)
    db.session.add(user)
    db.session.commit()
    return user


def test_user_creation(client, init_database):
    assert User.query.count() == 0
    user = create_user()
    assert User.query.count() == 1
    assert user.password is not EXAMPLE_PASSWORD

def test_get_register(client, init_database):
    response = client.get(url_for('users.register'))
    assert response.status_code == 200
    assert 'Реєстрація'.encode() in response.data
    assert 'Email'.encode() in response.data
    assert 'Пароль'.encode() in response.data

def test_register(client, init_database):
    response = client.post('/register', data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'Реєстрація пройшла успішно'.encode() in response.data
    assert EXAMPLE_EMAIL in str(response.data)
    assert b'BookShop' in response.data 