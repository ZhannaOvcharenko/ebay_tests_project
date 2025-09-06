import logging
import os
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
    """
    Базовый URL eBay API (sandbox или production)
    """
    return os.getenv("EBAY_API_URL", "https://api.sandbox.ebay.com")


@pytest.fixture(scope="session")
def auth_data():
    """
    Возвращает requests.Session с заголовком Authorization
    """
    session = get_auth_token()
    return session
