import os
import requests
from dotenv import load_dotenv

load_dotenv()


# ============ Helpers ============

def _load_tokens():
    return {
        "client_id": os.getenv("EBAY_CLIENT_ID"),
        "client_secret": os.getenv("EBAY_CLIENT_SECRET"),
        "refresh_token": os.getenv("EBAY_REFRESH_TOKEN"),
    }


def get_app_session():
    """client_credentials flow (application token)."""
    tokens = _load_tokens()
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "scope": "https://api.ebay.com/oauth/api_scope"
    }
    r = requests.post(
        url,
        headers=headers,
        data=data,
        auth=(tokens["client_id"], tokens["client_secret"])
    )
    r.raise_for_status()
    access_token = r.json()["access_token"]
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session


def get_user_session_from_refresh_token():
    """user access token через refresh_token (для Watchlist API)."""
    tokens = _load_tokens()
    url = "https://api.ebay.com/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"],
        "scope": "https://api.ebay.com/oauth/api_scope https://api.ebay.com/oauth/api_scope/buy.watchlist"
    }
    r = requests.post(
        url,
        headers=headers,
        data=data,
        auth=(tokens["client_id"], tokens["client_secret"])
    )
    r.raise_for_status()
    access_token = r.json()["access_token"]
    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session


# ============ Backward compatibility ============

def get_auth_token():
    """Alias для старого кода. Возвращает application session."""
    return get_app_session()


# ============ Public API ============

def load_tokens():
    """Публичная обёртка для загрузки токенов из .env"""
    return _load_tokens()
