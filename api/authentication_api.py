import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode

load_dotenv()

CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("EBAY_REDIRECT_URI", "https://localhost")
SCOPE = os.getenv("EBAY_SCOPE", "https://api.ebay.com/oauth/api_scope")
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.sandbox.ebay.com")
TOKEN_FILE = os.path.join(os.path.dirname(__file__), ".ebay_token")


def save_tokens(access_token, refresh_token=None):
    """Сохраняем токены в файл"""
    data = {"access_token": access_token}
    if refresh_token:
        data["refresh_token"] = refresh_token
    with open(TOKEN_FILE, "w") as f:
        f.write(str(data))


def load_tokens():
    """Загружаем токены из файла"""
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "r") as f:
            return eval(f.read())
    return {}


def get_auth_token(auth_type="client_credentials", auth_code=None):
    """Получение токена eBay и создание сессии requests.Session"""
    tokens = load_tokens()
    access_token = tokens.get("access_token")
    refresh_token = tokens.get("refresh_token")

    if access_token:
        session = requests.Session()
        session.headers.update({"Authorization": f"Bearer {access_token}"})
        return session

    url = f"{BASE_API_URL}/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    if auth_type == "client_credentials":
        data = {
            "grant_type": "client_credentials",
            "scope": SCOPE
        }
        response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))

    elif auth_type == "auth_code":
        if not auth_code and not refresh_token:
            raise ValueError("auth_code или refresh_token нужен для Authorization Code Flow")
        if refresh_token:
            data = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "scope": SCOPE
            }
        else:
            data = {
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": REDIRECT_URI
            }
        response = requests.post(url, headers=headers, data=data, auth=(CLIENT_ID, CLIENT_SECRET))

    else:
        raise ValueError("auth_type должен быть 'client_credentials' или 'auth_code'")

    response.raise_for_status()
    result = response.json()
    access_token = result["access_token"]
    refresh_token = result.get("refresh_token", refresh_token)
    save_tokens(access_token, refresh_token)

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {access_token}"})
    return session


def generate_auth_url(scope=None):
    if scope is None:
        scope = SCOPE
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": scope
    }
    return f"https://auth.sandbox.ebay.com/oauth2/authorize?{urlencode(params)}"