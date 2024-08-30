import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import pytest
from app import create_app, db

@pytest.fixture
def test_client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = 'testsecretkey'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(test_client):
    response = test_client.post('/api/register', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 201
    assert 'msg' in response.json

def test_login(test_client):
    test_client.post('/api/register', json={'username': 'testuser', 'password': 'testpassword'})
    response = test_client.post('/api/login', json={'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 200
    assert 'access_token' in response.json

def test_get_tasks_unauthenticated(test_client):
    response = test_client.get('/api/tasks')
    assert response.status_code == 401

def test_post_tasks_unauthenticated(test_client):
    response = test_client.post('/api/tasks', json={'title': 'New task', 'description': "test task", 'completed':False})
    assert response.status_code == 401

def test_authenticated_tasks(test_client):
    test_client.post('/api/register', json={'username': 'testuser', 'password': 'testpassword'})
    login_response = test_client.post('/api/login', json={'username': 'testuser', 'password': 'testpassword'})
    token = login_response.json['access_token']

    response = test_client.get('/api/tasks', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    response = test_client.post('/api/tasks', json={'title': 'New task', 'description': "test task", 'completed':False}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 201
    assert 'id' in response.json

    task_id = response.json['id']

    response = test_client.put(f'/api/tasks/{task_id}', json={'title': 'Updated task'}, headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    response = test_client.get(f'/api/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200
    assert response.json['title'] == 'Updated task'

    response = test_client.delete(f'/api/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 200

    response = test_client.get(f'/api/tasks/{task_id}', headers={'Authorization': f'Bearer {token}'})
    assert response.status_code == 404