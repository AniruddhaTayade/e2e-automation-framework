from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from config.config import TIMEOUT


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TIMEOUT)

    def find(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_clickable(self, locator):
        return self.wait.until(EC.element_to_be_clickable(locator))

    def find_all(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator):
        self.find_clickable(locator).click()

    def type(self, locator, text):
        el = self.find(locator)
        # Focus → set value via native setter → dispatch input+change events so
        # React controlled-component onChange handlers fire in headless Chrome too.
        self.driver.execute_script("arguments[0].focus()", el)
        self.driver.execute_script(
            "var nv = Object.getOwnPropertyDescriptor("
            "window.HTMLInputElement.prototype, 'value').set;"
            "nv.call(arguments[0], arguments[1]);"
            "arguments[0].dispatchEvent(new Event('input',  {bubbles:true}));"
            "arguments[0].dispatchEvent(new Event('change', {bubbles:true}));",
            el, text,
        )
        self.driver.execute_script("arguments[0].blur()", el)

    def get_text(self, locator) -> str:
        return self.find(locator).text

    def is_displayed(self, locator) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False

    @property
    def current_url(self) -> str:
        return self.driver.current_url
