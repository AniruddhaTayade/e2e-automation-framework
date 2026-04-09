from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from config.config import BASE_URL


class LoginPage(BasePage):
    _URL = BASE_URL
    _USERNAME = (By.ID, "user-name")
    _PASSWORD = (By.ID, "password")
    _LOGIN_BTN = (By.ID, "login-button")
    _ERROR_MSG = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self):
        self.driver.get(self._URL)
        return self

    def login(self, username: str, password: str):
        self.type(self._USERNAME, username)
        self.type(self._PASSWORD, password)
        self.click(self._LOGIN_BTN)

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MSG)

    def is_error_displayed(self) -> bool:
        return self.is_displayed(self._ERROR_MSG)
