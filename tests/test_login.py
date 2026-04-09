import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from config.config import USERS, BASE_URL


class TestLogin:
    def test_valid_login_redirects_to_inventory(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(USERS["standard"]["username"], USERS["standard"]["password"])

        inventory = InventoryPage(driver)
        assert "inventory" in driver.current_url
        assert inventory.get_page_title() == "Products"

    def test_invalid_password_shows_error(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(USERS["standard"]["username"], "wrong_password")

        assert login.is_error_displayed()
        assert "Username and password do not match" in login.get_error_message()

    def test_invalid_username_shows_error(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login("not_a_user", USERS["standard"]["password"])

        assert login.is_error_displayed()
        assert "Username and password do not match" in login.get_error_message()

    def test_empty_credentials_shows_error(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login("", "")

        assert login.is_error_displayed()
        assert "Username is required" in login.get_error_message()

    def test_locked_user_cannot_login(self, driver):
        login = LoginPage(driver)
        login.open()
        login.login(USERS["locked"]["username"], USERS["locked"]["password"])

        assert login.is_error_displayed()
        assert "locked out" in login.get_error_message().lower()

    def test_login_page_loads_at_base_url(self, driver):
        driver.get(BASE_URL)
        assert driver.current_url.rstrip("/") == BASE_URL.rstrip("/")
        login = LoginPage(driver)
        assert login.is_displayed((login._LOGIN_BTN[0], login._LOGIN_BTN[1]))
