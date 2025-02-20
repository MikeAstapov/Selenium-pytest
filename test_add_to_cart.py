import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import EMAIL, PASSWORD
import logging

site = "http://selenium1py.pythonanywhere.com/ru/catalogue/category/books_2/"
logging.basicConfig(filename="logs.log",level=logging.INFO)

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture
def authorization(driver):
    driver.get(site)
    driver.find_element(By.ID, "login_link").click()
    driver.find_element(By.ID, "id_login-username").send_keys(EMAIL)
    driver.find_element(By.ID, "id_login-password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[name='login_submit']").click()


class TestAuthPage:

    def test_main_page(self, driver):
        """Смок тесты"""
        driver.get(site)
        basket = driver.find_element(By.XPATH, '//*[@id="default"]/header/div[1]/div/div[2]/span/a')
        login_button = driver.find_element(By.ID, "login_link")
        assert basket.is_displayed(), "Корзина не найдена"
        assert login_button.is_displayed(), "Кнопка авторизации не найдена"

    def test_registration_successful(self, driver):
        """Проверка успешной регистрации."""
        driver.get(site)
        driver.find_element(By.ID, "login_link").click()
        driver.find_element(By.ID, "id_registration-email").send_keys(EMAIL)
        driver.find_element(By.ID, "id_registration-password1").send_keys(PASSWORD)
        driver.find_element(By.ID, "id_registration-password2").send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, "button[name='registration_submit']").click()

        try:
            # Ожидаем появления успешного сообщения
            success_element = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alertinner")))
            assert "Спасибо за регистрацию!" in success_element.text, \
                f"Ожидалось сообщение 'Спасибо за регистрацию!', но получено: {success_element.text}"



        except TimeoutException:

            # Если успешное сообщение не появилось, проверяем ошибку

            error_element = WebDriverWait(driver, 5).until(

                EC.visibility_of_element_located((By.CLASS_NAME, "alert-danger")))

            pytest.fail(f"Регистрация не удалась. Ошибка: {error_element.text}")
            driver.save_screenshot("test_fail_registration.png")

    def test_auth(self, authorization, driver):
        """Проверка успешной авторизации."""


        try:
            success_login = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "alertinner")))
            assert "Рады видеть вас снова" in success_login.text, \
                f"Ожидалось сообщение 'Рады видеть вас снова', но получено: {success_login.text}"

        except TimeoutException:
            pytest.fail("Авторизация не удалась: сообщение об успехе не появилось.")
            driver.save_screenshot("test_fail_login.png")


        def test_cart():
            """Проверка доступности корзины"""
            pass
