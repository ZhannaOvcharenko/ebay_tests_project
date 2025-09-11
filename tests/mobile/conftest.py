import os
import pytest
from appium import webdriver
from selene.support.shared import browser
from dotenv import load_dotenv
import config as cfg
from utils import attach


def pytest_addoption(parser):
    parser.addoption(
        "--context",
        default="bstack",
        help="Specify the test context"
    )


@pytest.fixture
def context(request):
    return request.config.getoption("--context")


@pytest.fixture(scope="function", autouse=True)
def mobile_management(context):
    """Фикстура для инициализации мобильного драйвера и закрытия сессии"""

    # Загружаем переменные окружения для выбранного контекста
    env_file_path = f".env.{context}"
    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        print(f"Warning: Configuration file '{env_file_path}' not found.")

    # Опции для драйвера
    options = cfg.to_driver_options(context=context)
    remote_url = options.get_capability("remote_url")
    if not remote_url:
        raise ValueError("REMOTE_URL is not set. Check your .env file.")

    # Инициализация драйвера
    browser.config.driver = webdriver.Remote(
        command_executor=remote_url,
        options=options
    )
    browser.config.timeout = 10.0

    yield

    # Вложения для Allure
    attach.add_screenshot(browser)
    attach.add_logs(browser)
    attach.add_html(browser)
    attach.add_video(browser)

    browser.close()
