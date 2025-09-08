import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
SCOPE = os.getenv("EBAY_SCOPE", "https://api.ebay.com/oauth/api_scope")

# URL для eBay API (sandbox или production из .env)
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.ebay.com")

# Файл для хранения токена
TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".ebay.token")


def save_token(access_token: str):
    """Сохраняет токен в файл"""
    with open(TOKEN_FILE, "w") as f:
        f.write(access_token)


def load_token() -> str | None:
    """Загружает токен из файла"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return f.read().strip()
    return None


def get_auth_token() -> requests.Session:
    """
    Возвращает requests.Session с заголовком Authorization Bearer.
    Используется flow client_credentials.
    """
    access_token = load_token()
    if access_token:
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {access_token}"})
        return session

    # Если токена нет — запрашиваем новый
    url = f"{BASE_API_URL}/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {"grant_type": "client_credentials", "scope": SCOPE}

    response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()
    result = response.json()
    access_token = result["access_token"]
    save_token(access_token)

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session
