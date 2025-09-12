import os
import pytest
from appium import webdriver
from dotenv import load_dotenv
from selene import browser
import config
from utils import attach


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    load_dotenv(".env.bstack")  # загружаем переменные для BrowserStack

    options = config.to_driver_options(context='bstack')

    browser.config.driver = webdriver.Remote(
        command_executor=os.getenv('REMOTE_URL'),
        options=options
    )
    browser.config.timeout = 10.0

    # Сохраняем креды в browser.config для использования в тестах
    browser.config.TEST_EBAY_USERNAME = os.getenv('TEST_EBAY_USERNAME')
    browser.config.TEST_EBAY_PASSWORD = os.getenv('TEST_EBAY_PASSWORD')
    browser.config.TEST_EBAY_WRONG_PASSWORD = os.getenv('TEST_EBAY_WRONG_PASSWORD')

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    browser.quit()
