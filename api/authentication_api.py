import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
SCOPE = os.getenv("EBAY_SCOPE", "https://api.ebay.com/oauth/api_scope")

# По умолчанию URL для SANDBOX
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.sandbox.ebay.com")

TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".ebay_token")


def save_tokens(access_token):
    with open(TOKEN_FILE, "w") as f:
        f.write(access_token)


def load_tokens():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read()
    return None


def get_auth_token():
    """Возвращает requests.Session с токеном client_credentials"""
    access_token = load_tokens()
    if access_token:
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {access_token}"})
        return session

    url = f"{BASE_API_URL}/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials", "scope": SCOPE}

    # Авторизация через Basic Auth
    response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()
    result = response.json()
    access_token = result["access_token"]
    save_tokens(access_token)

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session
