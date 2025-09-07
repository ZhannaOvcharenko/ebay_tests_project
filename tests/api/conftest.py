import os
import logging
import pytest
from api.authentication_api import get_auth_token, generate_auth_url


def pytest_configure():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("EBAY_API_URL", "https://api.sandbox.ebay.com")


@pytest.fixture(scope="session")
def auth_data():
    SCOPE = os.getenv("EBAY_SCOPE", "https://api.ebay.com/oauth/api_scope")

    if "buy.shopping.cart" in SCOPE or "buy.watchlist" in SCOPE:
        logging.info("Scope требует Authorization Code Flow.")
        session = get_auth_token(auth_type="auth_code", auth_code=os.getenv("EBAY_AUTH_CODE"))
    else:
        logging.info("Используем client_credentials flow.")
        session = get_auth_token(auth_type="client_credentials")

    return session
