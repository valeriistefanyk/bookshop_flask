import pytest
from flask import url_for

from bookshop.models import Book, User
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

def test_details_page(client, init_database, sample_book, authenticated_request):
  response = client.get(url_for('books.details', book_id=sample_book.id))
  assert response.status_code == 200
  assert 'BookShop' in str(response.data)
  assert '...' in str(response.data)

def test_not_found_page(client, init_database, authenticated_request):
  response = client.get(url_for('books.details', book_id=1))
  assert response.status_code == 404
  assert url_for('index') in str(response.data)

def test_creation(client, init_database, authenticated_request):
    response = client.post(url_for('books.create'),
                        data=TEST_BOOK,
                        follow_redirects=True)
    assert response.status_code == 200
    assert b'test title' in response.data
    assert b'BookShop' in response.data

def test_invalid_creation(client, init_database):
    response = client.post(url_for('books.create'),
                        data=dict(title=' s ', description='is not valid'),
                        follow_redirects=True)
    assert response.status_code == 200
    assert b'is not valid' in response.data
    assert b'Field must be between' in response.data
    assert b'is-invalid' in response.data

def test_edit_page(client, init_database, sample_book, authenticated_request):
    response = client.get(url_for('books.edit', book_id=sample_book.id))
    assert response.status_code == 200
    assert sample_book.description in str(response.data)
    assert sample_book.title in str(response.data)

def test_edit_submission(client, init_database, sample_book, authenticated_request):
    old_description = sample_book.description
    old_title = sample_book.title
    response = client.post(url_for('books.edit',
                        book_id=sample_book.id),
                        data={'title': 'test-change', 'description': 'is persisted'},
                        follow_redirects=True)
    assert response.status_code == 200
    assert 'test-change' in str(response.data)
    assert 'is persisted' in str(response.data)
    assert old_description not in str(response.data)
    assert old_title not in str(response.data)
