import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'})
    client = app.test_client()

    with app.app_context():
        db.create_all()

    yield client

    with app.app_context():
        db.drop_all()

def test_register(test_client):
    response = test_client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 201
    assert 'token' in response.json

def test_login(test_client):
    test_client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'token' in response.json

def test_get_tasks_unauthenticated(test_client):
    response = test_client.get('/tasks')
    assert response.status_code == 401

def test_post_tasks_unauthenticated(test_client):
    response = test_client.post('/tasks', json={'task': 'New task'})
    assert response.status_code == 401

def test_authenticated_tasks(test_client):
    test_client.post('/register', json={'username': 'testuser', 'password': 'testpassword'})
    login_response = test_client.post('/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = login_response.json['token']

    response = test_client.get('/tasks', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    response = test_client.post('/tasks', json={'task': 'New task'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'task_id' in response.json

    task_id = response.json['task_id']

    response = test_client.put(f'/tasks/{task_id}', json={'task': 'Updated task'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    response = test_client.get(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['task'] == 'Updated task'

    response = test_client.delete(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 204

    response = test_client.get(f'/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404