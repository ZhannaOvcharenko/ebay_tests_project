import logging
import pytest

from api.authentication_api import get_auth_token


@pytest.fixture(scope="session")
def base_url():
    """Базовый URL для API"""
    return "https://api.ebay.com"


@pytest.fixture(scope="session")
def prod_session():
    """Session для PROD с доступными scope (client_credentials)"""
    logging.info("Используем PROD session (client_credentials)")
    return get_auth_token()


@pytest.fixture(scope="session")
def sandbox_session():
    """Session для SANDBOX (можно заменить на альтернативный endpoint)"""
    logging.info("Используем SANDBOX session (client_credentials)")
    return get_auth_token()
    # Если позже будет refresh_token для sandbox, можно заменить на:
    # return get_user_session_from_refresh_token()


@pytest.fixture
def auth_data(request, prod_session, sandbox_session):
    """
    Автоматический выбор session в зависимости от маркера:
    - @pytest.mark.prod → prod_session
    - @pytest.mark.sandbox → sandbox_session
    """
    if "prod" in request.keywords:
        return prod_session
    elif "sandbox" in request.keywords:
        return sandbox_session
    else:
        # По умолчанию используем prod
        return prod_session
