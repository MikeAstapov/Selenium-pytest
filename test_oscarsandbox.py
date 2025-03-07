import pytest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config import EMAIL, PASSWORD

URL = "http://selenium1py.pythonanywhere.com/ru/catalogue/category/books_2/"


@pytest.fixture(scope="function", autouse=True)
def driver():
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--headless=new') # Закомментировать строку, если хотите видеть открытия браузера.
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def authorization(driver):
    driver.get(URL)
    driver.find_element(By.ID, "login_link").click()
    driver.find_element(By.ID, "id_login-username").send_keys(EMAIL)
    driver.find_element(By.ID, "id_login-password").send_keys(PASSWORD)
    driver.find_element(By.CSS_SELECTOR, "button[name='login_submit']").click()


class TestAuthPage:
    @pytest.mark.smoke
    def test_main_page(self, driver):
        """Смок тесты"""
        driver.get(URL)
        basket = driver.find_element(By.XPATH, '//*[@id="default"]/header/div[1]/div/div[2]/span/a')
        login_button = driver.find_element(By.ID, "login_link")
        assert basket.is_displayed(), "Корзина не найдена"
        assert login_button.is_displayed(), "Кнопка авторизации не найдена"

    def test_registration_successful(self, driver):
        """Проверка успешной регистрации."""
        driver.get(URL)
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

    @pytest.mark.smoke
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


class TestCart:
    @pytest.mark.smoke
    def test_cart(self, authorization, driver):
        """Проверка доступности корзины"""
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='default']/header/div[1]/div/div[2]/span/a"))).click()
        cart = driver.find_element(By.CLASS_NAME, "page-header>h1")
        assert "Корзина" == cart.text

    def add_item_to_cart(self, driver):
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CLASS_NAME, "dropdown-submenu"))).click()

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH,
                                              "//*[@id='default']/div[2]/div/div/div/section/div/ol/li[1]/article/div[2]/form/button"))).click()
        item_add = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='messages']/div[1]/div")))
        assert "был добавлен в вашу корзину" in item_add.text, f"Товар по какой-то причине не добавлен в корзину. Ошибка: {item_add.text}"

        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='default']/header/div[1]/div/div[2]/span/a"))).click()

    def test_add_item_to_cart(self, authorization, driver):
        """Проверка добавления 1 товара в корзину"""

        self.add_item_to_cart(driver)

        button_for_buy = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "#content_inner > div.form-group.clearfix > div > div > a")))
        assert button_for_buy.is_displayed(), "Кнопка оформления заказа не найдена. Возможно корзина пуста!"

    def test_final_order(self, authorization, driver):
        """Проверка оформления заказа"""
        self.add_item_to_cart(driver)
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "btn.btn-lg.btn-primary.btn-block"))).click()
        WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "option[value='Mr']"))).click()
        driver.find_element(By.ID, "id_first_name").send_keys("Михаил")
        driver.find_element(By.ID, "id_last_name").send_keys("Петров")
        driver.find_element(By.ID, "id_line1").send_keys("Гагарина 8/1")
        driver.find_element(By.ID, "id_line4").send_keys("Москва")
        driver.find_element(By.ID, "id_postcode").send_keys("141333")
        driver.find_element(By.CSS_SELECTOR, "option[value='RU']").click()
        driver.find_element(By.CLASS_NAME, "btn.btn-lg.btn-primary").click()
        final_step = driver.find_element(By.CLASS_NAME, "sub-header")
        assert "Введите параметры платежа" in final_step.text, f"Что-то пошло не так. Возможно не было заполнено обязательное поле"

    def test_clear_cart(self, authorization, driver):
        """Очистка корзины от товаров"""
        try:
            WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//*[@id='default']/header/div[1]/div/div[2]/span/a"))).click()
            input_field = WebDriverWait(driver, 5).until(
                (EC.visibility_of_element_located((By.ID, "id_form-0-quantity"))))
            input_field.clear()
            input_field.send_keys("0")
            driver.find_element(By.CSS_SELECTOR, "button[data-loading-text='Обновление...']").click()
            update_cart = driver.find_element(By.CSS_SELECTOR, ".alertinner p:first-child")
            assert "Ваша корзина теперь пуста" in update_cart.text, "Что-то пошло не так, и корзина не пуста"
        except TimeoutException:
            pytest.fail("Корзина была пуста!")


class TestOtherFunctions:
    @pytest.mark.smoke
    def test_search(self, driver):
        driver.get(URL)
        """Проверка функции поиска по сайту"""
        WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, "id_q"))).send_keys(
            "work")
        driver.find_element(By.CSS_SELECTOR, ".btn.btn-default[value='Найти']").click()
        try:
            response = WebDriverWait(driver, 5).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "product_price")))
            assert response, "Что-то пошло не так в позитивном сценарии!"
        except TimeoutException:
            pytest.fail("Поиск отработал с ошибкой")
