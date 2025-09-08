import os
import logging
import pytest
from api.authentication_api import get_auth_token


def pytest_configure():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


@pytest.fixture(scope="session")
def base_url():
    # Берем URL из .env, по умолчанию production
    return os.getenv("EBAY_API_URL", "https://api.ebay.com")


@pytest.fixture(scope="session")
def auth_data():
    logging.info("Используем client_credentials flow для eBay API.")
    # Возвращаем сессию с токеном
    session = get_auth_token()
    return session
