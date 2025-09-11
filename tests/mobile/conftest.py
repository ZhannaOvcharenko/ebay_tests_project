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
        help="Specify the test context: 'bstack' or 'local'"
    )


def pytest_configure(pytest_config: pytest.Config):
    """Загрузка переменных окружения из .env файла в зависимости от контекста"""
    context = pytest_config.getoption("--context", default="bstack")
    env_file_path = f".env.{context}"
    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        print(f"Warning: Configuration file '{env_file_path}' not found.")


@pytest.fixture
def context(request):
    """Фикстура для получения контекста запуска"""
    return request.config.getoption("--context")


@pytest.fixture(scope='function', autouse=True)
def mobile_management(context):
    """Фикстура для управления мобильным браузером/приложением"""
    options = config.to_driver_options(context=context)
    remote_url = options.get_capability('remote_url')

    # Инициализация WebDriver
    browser.config.driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )
    browser.config.timeout = 10.0

    yield

    # После теста делаем вложения в Allure
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.close()
