import os
import requests
from dotenv import load_dotenv

load_dotenv()


def _load_tokens(env="prod"):
    if env == "sandbox":
        return {
            "client_id": os.getenv("EBAY_SANDBOX_CLIENT_ID"),
            "client_secret": os.getenv("EBAY_SANDBOX_CLIENT_SECRET"),
            "refresh_token": os.getenv("EBAY_SANDBOX_REFRESH_TOKEN"),
        }
    return {
        "client_id": os.getenv("EBAY_CLIENT_ID"),
        "client_secret": os.getenv("EBAY_CLIENT_SECRET"),
        "refresh_token": os.getenv("EBAY_REFRESH_TOKEN"),
    }


def get_app_session(env="prod"):
    """Client credentials flow (application token)."""
    tokens = _load_tokens(env)
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    r = requests.post(url, headers=headers, data=data,
                      auth=(tokens["client_id"], tokens["client_secret"]))
    r.raise_for_status()
    access_token = r.json()["access_token"]
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session


def get_user_session_from_refresh_token(env="prod"):
    """User access token через refresh_token (для Watchlist API)."""
    tokens = _load_tokens(env)
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    scope = "https://api.ebay.com/oauth/api_scope"
    if env == "sandbox":
        scope += " https://api.ebay.com/oauth/api_scope/buy.watchlist"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "scope": scope
    }

    r = requests.post(url, headers=headers, data=data,
                      auth=(tokens["client_id"], tokens["client_secret"]))
    r.raise_for_status()
    access_token = r.json()["access_token"]
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session


# ============ Backward compatibility ============

def get_auth_token(env="prod"):
    """Alias для старого кода. Возвращает application session."""
    return get_app_session(env)


def load_tokens(env="prod"):
    """Публичная обёртка для загрузки токенов из .env"""
    return _load_tokens(env)
