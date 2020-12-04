import pytest
from flask import url_for

from bookshop import db
from bookshop import create_app
from bookshop.models import User


@pytest.fixture
def app():
    return create_app('test')


@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()

@pytest.fixture
def authenticated_request(client):
    new_user = User.create('test@example.com', 'examplepass')
    db.session.add(new_user)
    db.session.commit()
    response = client.post(url_for('users.login'), data={
            'email': 'test@example.com',
            'password': 'examplepass',
        }, follow_redirects=True)
    yield client

@pytest.fixture
def set_language_in_session(client):
    with client.session_transaction() as session:
        session['language'] = 'en'
    yield client