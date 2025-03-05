from http.client import responses

import requests
import pytest

from config import USERNAME, PASSWORD_booker, URL_BOOKS, HEADERS


def test_auth_func():
    data = {
        "username": USERNAME,
        "password": PASSWORD_booker
    }
    response = requests.post("https://restful-booker.herokuapp.com/auth", data=data)
    try:
        token = response.json()['token']
        assert response.status_code == 200 and token
    except KeyError:
        pytest.fail(f"Ошибка авторизации : {response.json()["reason"]}")


@pytest.fixture()
def create_book():
    data = {
        "firstname": "Michael",
        "lastname": "Astapov",
        "totalprice": 999,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-01-01",
            "checkout": "2025-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post("https://restful-booker.herokuapp.com/booking", json=data).json()
    yield response["bookingid"]
    requests.delete(f"https://restful-booker.herokuapp.com/booking/{response['bookingid']}", headers=HEADERS)


def test_get_booking_ids(create_book):
    response = requests.get(f"{URL_BOOKS}/booking/{create_book}").json()
    assert response["firstname"] == "Michael" and response["lastname"] == "Astapov" and response[
        "totalprice"] == 999, f"Id {create_book} не найден"


def test_put_book(create_book):
    data = {
        "firstname": "James",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.put(f"{URL_BOOKS}/booking/{create_book}", json=data, headers=HEADERS).json()
    assert response['firstname'] == 'James' and response['lastname'] == 'Brown' and response[
        'totalprice'] == 111, "Обновление данных вызвало ошибку"


def test_patch_book(create_book):
    data = {"firstname": "TEST NAME",
            "lastname": "TEST SURNAME"}
    response = requests.patch(f"{URL_BOOKS}/booking/{create_book}", json=data, headers=HEADERS).json()
    assert response['firstname'] == 'TEST NAME' and response[
        'lastname'] == 'TEST SURNAME', "Частичное обновление данных вызвало ошибку"


def test_delete_book(create_book):
    requests.delete(f"https://restful-booker.herokuapp.com/booking/{create_book}", headers=HEADERS)
    print(create_book)
    response = requests.get(f"{URL_BOOKS}/booking/{create_book}")
    assert response.status_code == 404, f"Запись не была удалена. Id книги {create_book}"
