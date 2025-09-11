import os
import logging
import pytest
import requests
from api.authentication_api import get_auth_token, get_user_session_from_refresh_token, load_tokens


@pytest.fixture(scope="session")
def base_url():
    env = os.getenv("EBAY_ENV", "prod")
    if env == "sandbox":
        return os.getenv("EBAY_SANDBOX_API_URL")
    return os.getenv("EBAY_API_URL")


@pytest.fixture(scope="session")
def auth_data():
    """
    Выбор авторизации:
    - prod: client_credentials flow для доступного scope
    - sandbox: имитация с базовым session (без реального user token)
    """
    env = os.getenv("EBAY_ENV", "prod")
    tokens = load_tokens()
    if env == "sandbox":
        logging.info("Sandbox environment: создаём базовую сессию без refresh token")
        session = requests.Session()
        session.headers.update({"Authorization": "Bearer MOCK_SANDBOX_TOKEN"})
        return session

    # Prod environment
    if os.getenv("EBAY_REFRESH_TOKEN") or tokens.get("refresh_token"):
        logging.info("Используем user-token (refresh_token flow) для eBay API.")
        return get_user_session_from_refresh_token()
    logging.info("Используем client_credentials flow для eBay API.")
    return get_auth_token()
