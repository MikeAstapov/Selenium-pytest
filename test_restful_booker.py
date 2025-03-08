import requests
import pytest

from config import USERNAME, PASSWORD_booker, URL_BOOKS, HEADERS, data_create_method, data_put_method


@pytest.fixture(scope="module")
def create_book():
    response = requests.post("https://restful-booker.herokuapp.com/booking", json=data_create_method).json()
    yield response["bookingid"]
    requests.delete(f"https://restful-booker.herokuapp.com/booking/{response['bookingid']}", headers=HEADERS)


class TestGetMethods:

    def test_get_booking_ids_positive(self, create_book):
        response = requests.get(f"{URL_BOOKS}/booking/{create_book}").json()
        assert response["firstname"] == "Michael" and response["lastname"] == "Astapov" and response[
            "totalprice"] == 999, f"Id {create_book} не найден"


class TestPostMethods:

    def test_auth_func_positive(self):
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


class TestPutMethods:

    def test_put_book_positive(self, create_book):

        response = requests.put(f"{URL_BOOKS}/booking/{create_book}", json=data_put_method, headers=HEADERS).json()
        assert response['firstname'] == 'James' and response['lastname'] == 'Brown' and response[
            'totalprice'] == 111, "Обновление данных вызвало ошибку"

    def test_put_book_without_id_negative(self, create_book):
        response = requests.put(f"{URL_BOOKS}/booking/999999999999999", json=data_put_method, headers=HEADERS)
        assert response.status_code == 405, "Успешный ответ об удалении несуществующей записи"

    def test_put_book_without_token_negative(self, create_book):
        response = requests.put(f"{URL_BOOKS}/booking/{create_book}", json=data_put_method)
        assert response.status_code == 403, "Успешное изменение записи без прав доступа"


class TestPatchMethods:

    def test_patch_book_positive(self, create_book):
        data = {"firstname": "TEST NAME",
                "lastname": "TEST SURNAME"}
        response = requests.patch(f"{URL_BOOKS}/booking/{create_book}", json=data, headers=HEADERS).json()
        assert response['firstname'] == 'TEST NAME' and response[
            'lastname'] == 'TEST SURNAME', "Частичное обновление данных вызвало ошибку"


class TestDeleteMethods:

    def test_delete_book_positive(self, create_book):
        requests.delete(f"https://restful-booker.herokuapp.com/booking/{create_book}", headers=HEADERS)
        response = requests.get(f"{URL_BOOKS}/booking/{create_book}")
        assert response.status_code == 404, f"Запись не была удалена. Id книги {create_book}"

    def test_delete_book_without_token_negative(self, create_book):
        # Тест без HEADERS, в которых есть bearer токен
        responce = requests.delete(f"https://restful-booker.herokuapp.com/booking/{create_book}")
        assert responce.status_code == 403, "Удалено без права доступа к методу"

    def test_delete_book_without_id_negative(self, create_book):
        # Тест удаление несуществующей записи с id=999999999999
        responce = requests.delete(f"https://restful-booker.herokuapp.com/booking/999999999999", headers=HEADERS)
        assert responce.status_code == 405, "Успешный ответ об удалении несуществующей записи"
