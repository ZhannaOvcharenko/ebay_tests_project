import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selene.support.shared import browser
from utils import attach
from dotenv import load_dotenv
from pages.main_page import MainPage

load_dotenv()


@pytest.fixture(scope='function', autouse=True)
def setup_browser():
    """Фикстура для настройки браузера и подключения к Selenoid"""
    selenoid_login = os.getenv("SELENOID_LOGIN")
    selenoid_pass = os.getenv("SELENOID_PASS")
    selenoid_url = os.getenv("SELENOID_URL")

    if not all([selenoid_login, selenoid_pass, selenoid_url]):
        raise ValueError(
            "Ошибка: переменные SELENOID_LOGIN, SELENOID_PASS или SELENOID_URL не заданы. "
            "Убедитесь, что .env существует или переменные переданы в окружение (например, через Jenkins)."
        )

    options = Options()
    selenoid_capabilities = {
        "browserName": "chrome",
        "browserVersion": "128.0",
        "selenoid:options": {
            "enableVNC": True,
            "enableVideo": True
        }
    }
    options.capabilities.update(selenoid_capabilities)

    driver = webdriver.Remote(
        command_executor=f"https://{selenoid_login}:{selenoid_pass}@{selenoid_url}/wd/hub",
        options=options
    )

    browser.config.driver = driver
    browser.config.base_url = "https://www.ebay.com/?geoip=US"
    browser.driver.maximize_window()
    browser.config.timeout = 10

    yield

    # Добавляем вложения в Allure
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()


@pytest.fixture()
def open_main_page():
    """Фикстура для открытия главной страницы и принятия cookies"""
    page = MainPage()
    page.open_ebay_main_page().accept_cookies_if_present()
    return page
