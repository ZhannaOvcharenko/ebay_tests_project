import logging
import pytest
from api.authentication_api import get_auth_cookie


def pytest_configure():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


@pytest.fixture(scope="session")
def auth_data():
    session, cookie = get_auth_cookie()
    session.cookies.set("ebay-session", cookie)
    return session
