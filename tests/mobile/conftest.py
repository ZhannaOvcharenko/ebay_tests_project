import os
import pytest
from appium import webdriver
from selene import browser
from dotenv import load_dotenv
import config
from utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Specify the test context"
    )


def pytest_configure(config_):
    context = config_.getoption("--context")
    env_file_path = f".env.{context}"

    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        print(f"Warning: Configuration file '{env_file_path}' not found.")


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope='function', autouse=True)
def mobile_management(context):
    options = config.to_driver_options(context=context)

    browser.config.driver = webdriver.Remote(
        command_executor=options.get_capability('remote_url'),
        desired_capabilities=options
    )
    browser.config.timeout = 10.0

    yield

    attach.add_screenshot(browser)
    attach.add_xml(browser)

    browser.quit()
