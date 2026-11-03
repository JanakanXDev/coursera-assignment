import json

from app import app


client = app.test_client()


def test_root_route():
    response = client.get('/')
    assert response.status_code == 200
    payload = json.loads(response.data.decode('utf-8'))
    assert 'OpenShift CI/CD Pipeline' in payload['name']


def test_health_route():
    response = client.get('/health')
    assert response.status_code == 200
    payload = json.loads(response.data.decode('utf-8'))
    assert payload['status'] == 'ok'
    assert payload['database'] in {'connected', 'disconnected'}


def test_list_products():
    response = client.get('/api/products')
    assert response.status_code == 200
    payload = json.loads(response.data.decode('utf-8'))
    assert isinstance(payload, list)
    assert len(payload) >= 1


def test_get_product_by_id():
    response = client.get('/api/products/1')
    assert response.status_code == 200
    payload = json.loads(response.data.decode('utf-8'))
    assert payload['id'] == 1
    assert 'name' in payload


def test_create_product():
    payload = {
        'name': 'USB-C Dock',
        'description': '7-port USB-C docking station',
        'price': 89.99,
        'category': 'Accessories',
    }
    response = client.post('/api/products', json=payload)
    assert response.status_code == 201
    response_payload = json.loads(response.data.decode('utf-8'))
    assert response_payload['name'] == 'USB-C Dock'


def test_update_product():
    payload = {'name': 'USB-C Dock Pro', 'price': 99.99}
    response = client.put('/api/products/1', json=payload)
    assert response.status_code == 200
    response_payload = json.loads(response.data.decode('utf-8'))
    assert response_payload['name'] == 'USB-C Dock Pro'


def test_delete_product():
    payload = {
        'name': 'Delete Me Product',
        'description': 'Temporary product for deletion test',
        'price': 10.5,
        'category': 'Testing',
    }
    create_response = client.post('/api/products', json=payload)
    product_id = json.loads(create_response.data.decode('utf-8'))['id']

    delete_response = client.delete(f'/api/products/{product_id}')
    assert delete_response.status_code == 200
    assert 'deleted successfully' in json.loads(delete_response.data.decode('utf-8'))['message']
