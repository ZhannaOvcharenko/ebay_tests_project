import logging
import os
import pytest

from api.authentication_api import (
    get_auth_token,
    get_user_session_from_refresh_token,
    load_tokens
)


@pytest.fixture(scope="session")
def base_url():
    return "https://api.ebay.com"


@pytest.fixture(scope="session")
def auth_data():
    """
    Выбор авторизации:
    - если есть refresh_token → используем user session
    - иначе используем client_credentials
    """
    tokens = load_tokens()
    if os.getenv("EBAY_REFRESH_TOKEN") or tokens.get("refresh_token"):
        logging.info("Используем user-token (refresh_token flow) для eBay API.")
        return get_user_session_from_refresh_token()

    logging.info("Используем client_credentials flow для eBay API.")
    return get_auth_token()
