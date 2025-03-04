import requests
import pytest


@pytest.fixture()
def create_obj_id():
    payload = {
        "name": "Apple Iphone Pro 16",
        "data": {
            "year": 2025,
            "price": 1000,
            "CPU model": "M2",
            "Hard disk size": "1 TB"
        }
    }
    response = requests.post('https://api.restful-api.dev/objects', json=payload).json()
    yield response["id"]
    requests.delete('https://api.restful-api.dev/objects', json=response)


@pytest.mark.smoke
def test_get_all_obj():
    response = requests.get('https://api.restful-api.dev/objects')
    assert response.status_code == 200


def test_post_obj():
    payload = {
        "name": "Apple Iphone Pro 16",
        "data": {
            "year": 2025,
            "price": 1000,
            "CPU model": "M2",
            "Hard disk size": "1 TB"
        }
    }
    res = requests.post('https://api.restful-api.dev/objects', json=payload).json()
    assert payload["name"] == res["name"]


def test_get_obj(create_obj_id):
    response = requests.get(f'https://api.restful-api.dev/objects/{create_obj_id}').json()
    assert create_obj_id == response["id"]


def test_put_obj(create_obj_id):
    payload = {
        "name": "TEST Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "TEST1 Intel Core i9",
            "Hard disk size": "TEST 1 TB"
        }
    }
    response = requests.put(f'https://api.restful-api.dev/objects/{create_obj_id}', json=payload).json()

    assert payload["name"] == response["name"]
    assert payload["data"]["CPU model"] == response["data"]["CPU model"]
    assert payload["data"]["Hard disk size"] == response["data"]["Hard disk size"]


def test_patch_obj(create_obj_id):
    payload = {
        "name": "TEST PATCH METHOD",
    }
    response = requests.patch(f'https://api.restful-api.dev/objects/{create_obj_id}', json=payload).json()
    assert payload["name"] == response["name"]


def test_delete_obj(create_obj_id):
    response = requests.delete(f'https://api.restful-api.dev/objects/{create_obj_id}')
    assert response.status_code == 200
    response = requests.get(f'https://api.restful-api.dev/objects/{create_obj_id}')
    assert response.status_code == 404
