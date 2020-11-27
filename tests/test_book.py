import pytest

from bookshop.models import Book
from bookshop.extenstions import db


TEST_BOOK = {
    'title': 'test title',
    'description': 'test description'
}


def test_book_creation(client, init_database):
    assert Book.query.count() == 0
    book = Book(**TEST_BOOK)
    db.session.add(book)
    db.session.commit()
    assert Book.query.count() == 1
    assert Book.query.first().title == TEST_BOOK['title']

def test_invalid_title_book_creation(client, init_database):
    with pytest.raises(ValueError):
        Book(title='  w  ', description='invalid title')