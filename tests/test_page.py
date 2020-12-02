import requests
from flask import url_for


def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'INDEX' in response.data

def test_not_found_page(client):
  response = client.get('/test')
  assert response.status_code == 404
  assert url_for('index') in str(response.data)