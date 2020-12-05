import pytest
from flask import url_for

from bookshop.models import User
from bookshop.extenstions import db


EXAMPLE_EMAIL = 'test@example.com'
EXAMPLE_PASSWORD = 'test123'
STORE_NAME = 'Test Store'

VALID_REGISTER_PARAMS = {
    'store_name': STORE_NAME,
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

def test_get_register(client, init_database, set_language_in_session):
    response = client.get(url_for('users.register'))
    assert response.status_code == 200
    assert 'Register'.encode() in response.data
    assert 'Email'.encode() in response.data
    assert 'Password'.encode() in response.data

def test_register(client, init_database, set_language_in_session):
    response = client.post(url_for('users.register'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'Registration successfully'.encode() in response.data
    assert EXAMPLE_EMAIL in str(response.data)
    assert b'BookShop' in response.data

def test_register_invalid(client, init_database, set_language_in_session):
    invalid_data = VALID_REGISTER_PARAMS.copy()
    invalid_data['email'] = 'abc'
    response = client.post(url_for('users.register'), data=invalid_data, follow_redirects=True)
    assert response.status_code == 200
    assert b'Invalid email' in response.data

def test_register_with_existing_user(client, init_database, set_language_in_session):
    user = create_user()
    response = client.post(url_for('users.register'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'An account with this email already exists'.encode() in response.data
    assert 'Registration successfully'.encode() not in response.data
    assert 'account is already registered'.encode() not in response.data

def test_already_logged_in_register(client, init_database, authenticated_request, set_language_in_session):
    response = client.post(url_for('users.register'), data=VALID_REGISTER_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'account is already registered'.encode() in response.data

def test_get_login(client, init_database, set_language_in_session):
    response = client.get(url_for('users.login'))
    assert response.status_code == 200
    assert 'Login'.encode() in response.data
    assert 'Email' in str(response.data)
    assert 'Password'.encode() in response.data
    assert 'confirm'.encode() not in response.data

def test_login(client, init_database, set_language_in_session):
    create_user()
    response = client.post(url_for('users.login'), data=VALID_LOGIN_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'Logged in successfully'.encode() in response.data
    assert url_for('users.logout') in str(response.data)

def test_already_logged_in_login(client, init_database, authenticated_request, set_language_in_session):
    response = client.post(url_for('users.login'), data=VALID_LOGIN_PARAMS, follow_redirects=True)
    assert response.status_code == 200
    assert 'You are already logged in'.encode() in response.data

def test_login_invalid_email(client, init_database, set_language_in_session):
    create_user()
    response = client.post(url_for('users.login'), data=dict(
        email="test",
        password=EXAMPLE_PASSWORD
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid email address' in str(response.data)

def test_login_no_user(client, init_database, set_language_in_session):
    create_user()
    response = client.post(url_for('users.login'), data=dict(
        email='test@notexistent.com',
        password=EXAMPLE_PASSWORD
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid email or password'.encode() in response.data

def test_login_bad_password(client, init_database, set_language_in_session):
    create_user()
    response = client.post(url_for('users.login'), data=dict(
        email=EXAMPLE_EMAIL,
        password='badpassword'
    ), follow_redirects=True)
    assert response.status_code == 200
    assert 'Invalid email or password'.encode() in response.data

def test_logout(client, init_database, authenticated_request):
    response = client.post(url_for('users.logout'), follow_redirects=True)
    assert response.status_code == 200
    assert url_for('users.login') in str(response.data)
    assert url_for('users.register') in str(response.data)
