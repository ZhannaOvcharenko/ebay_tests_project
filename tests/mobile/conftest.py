import pytest
import allure
from appium import webdriver
from config import mobile_config


@pytest.fixture(scope="function")
def driver():
    desired_caps = {
        "platformName": "Android",
        "deviceName": mobile_config.bstack_device,
        "os_version": mobile_config.bstack_os_version,
        "app": mobile_config.bstack_app,
        "project": mobile_config.project,
        "build": mobile_config.build,
        "name": mobile_config.name,
        "bstack:options": {
            "userName": mobile_config.bstack_user,
            "accessKey": mobile_config.bstack_key,
        },
    }

    driver = webdriver.Remote(
        command_executor="http://hub.browserstack.com/wd/hub",
        desired_capabilities=desired_caps
    )

    yield driver

    # Добавим вложения в allure
    allure.attach(
        driver.get_screenshot_as_png(),
        name="screenshot",
        attachment_type=allure.attachment_type.PNG
    )
    driver.quit()
