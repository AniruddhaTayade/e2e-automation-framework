import os
import pathlib
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager


def _resolve_chromedriver(raw_path: str) -> str:
    """webdriver-manager 4.x sometimes returns a non-exe file in the same dir.
    Walk up to the containing directory and find chromedriver(.exe)."""
    p = pathlib.Path(raw_path)
    exe_name = "chromedriver.exe" if os.name == "nt" else "chromedriver"
    candidate = p.parent / exe_name
    if candidate.exists():
        return str(candidate)
    return raw_path


def get_driver(browser: str = "chrome", headless: bool = False) -> webdriver.Remote:
    browser = browser.lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        if headless or os.getenv("CI"):
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")
        driver_path = _resolve_chromedriver(ChromeDriverManager().install())
        service = ChromeService(driver_path)
        return webdriver.Chrome(service=service, options=options)

    if browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless or os.getenv("CI"):
            options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)

    raise ValueError(f"Unsupported browser: {browser}")
