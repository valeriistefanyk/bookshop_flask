import pytest
from flask import url_for

from bookshop.models import Store, Book
from bookshop.extenstions import db

def create_store(name="Example Store", num_books = 0):
    store = Store(name=name)
    for index in range(num_books):
        book = Book(title=f"Book {index}", 
                    description=f"Example book description {index}",
                    store=store
        )
        db.session.add(book)
    db.session.add(store)
    db.session.commit()
    return store


# Unit Tests
def test_store_creation(client, init_database):
    assert Store.query.count() == 0
    assert Book.query.count() == 0
    store = create_store(num_books=3)
    assert Store.query.count() == 1
    assert Book.query.count() == 3
    for book in Book.query.all():
        assert book.store == store

# Functional Tests
def test_index_page(client, init_database):
  store = create_store(num_books=5)
  response = client.get(url_for('store.index'))
  assert response.status_code == 200
  assert b'BookShop' in response.data
  assert store.name in str(response.data)

  expected_link = url_for('store.show', store_id=store.id)
  assert expected_link in str(response.data)
  for book in store.books[:3]:
    expected_link = url_for('books.details', book_id=book.id)
    assert expected_link in str(response.data)

  for book in store.books[3:5]:
    expected_link = url_for('books.details', book_id=book.id)
    assert expected_link not in str(response.data)

def test_name_validation(client, init_database):
  assert Store.query.count() == 0
  with pytest.raises(ValueError):
    create_store(name=" * ")
  assert Store.query.count() == 0

def test_store_page(client, init_database):
  store = create_store(num_books=3)
  response = client.get(url_for('store.show', store_id=store.id))
  assert response.status_code == 200
  assert b'BookShop' in response.data
  assert store.name in str(response.data)

  for book in store.books:
    expected_link = url_for('books.details', book_id=book.id)
    assert expected_link in str(response.data)