import os
import pytest
from appium import webdriver
from dotenv import load_dotenv


@pytest.fixture(scope="function")
def driver():
    """
    Фикстура для инициализации мобильного драйвера и закрытия сессии.
    Работает с BrowserStack через .env.bstack
    """
    # Загружаем .env для BrowserStack
    env_file_path = ".env.bstack"
    if os.path.exists(env_file_path):
        load_dotenv(dotenv_path=env_file_path)
    else:
        raise FileNotFoundError(f"Файл конфигурации '{env_file_path}' не найден.")

    # Получаем переменные окружения
    remote_url = os.getenv("REMOTE_URL")
    platform_name = os.getenv("PLATFORM_NAME")
    device_name = os.getenv("DEVICE_NAME")
    platform_version = os.getenv("PLATFORM_VERSION")
    app_url = os.getenv("APP_URL")
    automation_name = os.getenv("AUTOMATION_NAME", "UiAutomator2")  # по умолчанию Android

    if not remote_url:
        raise ValueError("REMOTE_URL не задан в .env.bstack")

    # Формируем capabilities
    capabilities = {
        "platformName": platform_name,
        "deviceName": device_name,
        "platformVersion": platform_version,
        "automationName": automation_name,
        "app": app_url,
    }

    # Инициализация драйвера
    driver = webdriver.Remote(
        command_executor=remote_url,
        desired_capabilities=capabilities
    )

    yield driver

    # Закрываем сессию после теста
    driver.quit()
