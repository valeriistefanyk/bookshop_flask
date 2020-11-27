import pytest

from bookshop import db
from bookshop import create_app


@pytest.fixture
def app():
    return create_app('test')


@pytest.fixture
def init_database():
    db.create_all()
    yield
    db.drop_all()