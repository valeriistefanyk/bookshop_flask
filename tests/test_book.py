import pytest
from flask import url_for

from bookshop.models import Book
from bookshop.extenstions import db

TEST_BOOK = {
    'title': 'test title',
    'description': 'test description'
}

@pytest.fixture
def sample_book():
    book = Book(**TEST_BOOK)
    db.session.add(book)
    db.session.commit()
    return book


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

def test_index_page(client, init_database, sample_book):
    response = client.get(url_for('books.index'))
    assert response.status_code == 200
    assert 'BookShop' in str(response.data)
    assert sample_book.title in str(response.data)
  
    expected_link = url_for('books.details', book_id=sample_book.id)
    assert expected_link in str(response.data)

def test_details_page(client, init_database, sample_book):
  response = client.get(url_for('books.details', book_id=sample_book.id))
  assert response.status_code == 200
  assert 'BookShop' in str(response.data)
  assert '...' in str(response.data)

def test_not_found_page(client, init_database):
  response = client.get(url_for('books.details', book_id=1))
  assert response.status_code == 404
  assert url_for('index') in str(response.data)