import requests
from flask import url_for


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'INDEX' in response.data

def test_not_found_page(client, set_language_in_session):
  response = client.get('/test')
  assert response.status_code == 404
  assert url_for('index') in str(response.data)

def test_setting_language_session(client):
  response = client.get('/language/en')
  assert response.status_code == 302
  with client.session_transaction() as session:
      assert session['language'] == 'en'