from fastapi.testclient import TestClient
from src.main import app
from src.config.auth import verify_password
import random
import string


def test_create_login_get_delete_user_happy_path_e2e():
    client = TestClient(app)
    rand_string = ''.join((random.choice(string.ascii_letters)
                          for _ in range(5)))
    user_data = {
        'username': f'user_test_{rand_string}',
        'password': 'password_test'
    }

    # Create user
    response = client.post('/users/', json=user_data)
    assert response.status_code == 200

    # Check user created
    new_user = response.json()
    assert new_user['username'] == user_data['username']
    assert verify_password(user_data['password'], new_user['password'])

    # Login user
    response = client.post(
        '/login/', headers={'content-type': 'application/x-www-form-urlencoded'}, data=user_data)
    assert response.status_code == 200

    # Get token
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Get user
    response = client.get(f'/users/', headers=headers)
    assert response.status_code == 200

    obtained_user = response.json()
    assert obtained_user == new_user

    # Delete user
    response = client.delete(f'/users/', headers=headers)
    assert response.status_code == 200
