import os
import pytest
from appium import webdriver
from selene import browser
from dotenv import load_dotenv
import config
from utils import attach


@pytest.fixture(scope='function', autouse=True)
def mobile_management():
    load_dotenv(".env.bstack")

    options = config.to_driver_options(context='bstack')

    browser.config.driver = webdriver.Remote(
        command_executor=os.getenv("REMOTE_URL"),
        options=options
    )
    browser.config.timeout = 10.0

    yield

    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.quit()
