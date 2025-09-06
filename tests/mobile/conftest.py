import os
import pytest
from appium import webdriver
from selene import browser
from dotenv import load_dotenv
import config
from utils.attach import add_screenshot, add_logs, add_html, add_video


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
    remote_url = options.pop_capability('remote_url')

    # Создание сессии
    browser.config.driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )
    browser.config.timeout = 10.0

    yield

    # Добавление вложений для Allure
    add_screenshot(browser)
    add_logs(browser)
    add_html(browser)
    add_video(browser)

    # Закрытие сессии браузера
    browser.close()
