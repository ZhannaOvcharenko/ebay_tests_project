import os
import pytest
from appium import webdriver
from selene.support.shared import browser
from dotenv import load_dotenv

load_dotenv(".env.bstack")


@pytest.fixture(scope="function", autouse=True)
def setup_browserstack():
    desired_caps = {
        "platformName": "Android",
        "deviceName": os.getenv("DEVICE_NAME", "Google Pixel 6"),
        "app": os.getenv("APP_URL"),
        "appWaitActivity": os.getenv("APP_WAIT_ACTIVITY", "*"),
        "autoGrantPermissions": True,
    }

    driver = webdriver.Remote(
        command_executor=(
            f"https://{os.getenv('BSTACK_USER')}:"
            f"{os.getenv('BSTACK_KEY')}@hub.browserstack.com/wd/hub"
        ),
        desired_capabilities=desired_caps
    )

    browser.config.driver = driver

    yield browser

    driver.quit()
