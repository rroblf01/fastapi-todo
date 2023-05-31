from fastapi.testclient import TestClient
from src.main import app
from src.config.auth import verify_password
import random
import string


def test_create_get_delete_product_happy_path_e2e():
    client = TestClient(app)
    rand_string = ''.join((random.choice(string.ascii_letters)
                          for _ in range(5)))
    user_data = {
        'username': f'user_test_{rand_string}',
        'password': 'password_test'
    }

    # Create user
    response = client.post('/users/', json=user_data)

    # Get token
    response = client.post(
        '/login/', headers={'content-type': 'application/x-www-form-urlencoded'}, data=user_data)
    token = response.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}

    # Create product
    product_data = {
        'name': f'product_test_{rand_string}',
        'description': 'description_test',
        'price': 100
    }
    response = client.post('/products/', json=product_data, headers=headers)
    assert response.status_code == 200

    # Check product created
    new_product = response.json()
    assert new_product['name'] == product_data['name']
    assert new_product['description'] == product_data['description']
    assert new_product['price'] == product_data['price']

    # Get product
    response = client.get(f'/products/{new_product["id"]}', headers=headers)
    assert response.status_code == 200

    # Check product obtained
    obtained_product = response.json()
    assert obtained_product == new_product

    # Delete product
    response = client.delete(
        f'/products/{new_product["id"]}', headers=headers)
    assert response.status_code == 200

    # Delete user
    response = client.delete(f'/users/', headers=headers)
    assert response.status_code == 200
