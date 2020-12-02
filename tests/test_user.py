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

VALID_LOGIN_PARAMS = {
    'email': EXAMPLE_EMAIL,
    'password': EXAMPLE_PASSWORD
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
    response = client.post(url_for('users.register'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'Реєстрація пройшла успішно'.encode() in response.data
    assert EXAMPLE_EMAIL in str(response.data)
    assert b'BookShop' in response.data

def test_register_invalid(client, init_database):
    invalid_data = VALID_REGISTER_PARAMS.copy()
    invalid_data['email'] = 'abc'
    response = client.post(url_for('users.register'), data=invalid_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email' in response.data

def test_register_with_existing_user(client, init_database):
    user = create_user()
    response = client.post(url_for('users.register'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'Акаунт з цим email вже існує'.encode() in response.data
    assert 'Реєстрація пройшла успішно'.encode() not in response.data
    assert 'акаунт вже зареєстрований'.encode() not in response.data

def test_already_logged_in_register(client, init_database, authenticated_request):
    response = client.post(url_for('users.register'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'акаунт вже зареєстрований'.encode() in response.data
