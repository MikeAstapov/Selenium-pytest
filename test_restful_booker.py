from http.client import responses

import requests
import pytest

from config import USERNAME, PASSWORD_booker, URL_BOOKS, AUTHORIZATION


@pytest.fixture()
def auth_func():
    data = {
        "username": USERNAME,
        "password": PASSWORD_booker
    }
    response = requests.post("https://restful-booker.herokuapp.com/auth", data=data)
    token = response.json()['token']
    yield token


@pytest.fixture()
def create_book():
    headers = {

        "Authorization": AUTHORIZATION

    }
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
    requests.delete(f"https://restful-booker.herokuapp.com/booking/{response['bookingid']}", headers=headers)


def test_get_booking_ids(create_book):
    response = requests.get(f"{URL_BOOKS}/booking/{create_book}").json()
    print(create_book)
    assert response["firstname"] == "Michael" and response["lastname"] == "Astapov" and response[
        "totalprice"] == 999, f"Id {create_book} не найден"

#def test_create_book(create_book):

