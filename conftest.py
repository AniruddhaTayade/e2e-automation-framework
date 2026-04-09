import pytest
from utils.driver_factory import get_driver
from pages.login_page import LoginPage
from config.config import USERS


def pytest_addoption(parser):
    parser.addoption("--browser", default="chrome", help="Browser to run tests on")
    parser.addoption("--headless", action="store_true", default=False, help="Run headless")


@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")
    drv = get_driver(browser=browser, headless=headless)
    drv.maximize_window()
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def logged_in_driver(driver):
    """Driver fixture pre-authenticated as standard_user."""
    login = LoginPage(driver)
    login.open()
    login.login(USERS["standard"]["username"], USERS["standard"]["password"])
    return driver
