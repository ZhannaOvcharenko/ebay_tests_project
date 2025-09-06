import os
import requests
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("EBAY_CLIENT_ID")
CLIENT_SECRET = os.getenv("EBAY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("EBAY_REDIRECT_URI")
SCOPE = os.getenv("EBAY_SCOPE", "https://api.ebay.com/oauth/api_scope/buy.shopping.cart")
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.sandbox.ebay.com")


def get_auth_token():
    """
    Получение OAuth2 токена для eBay API (Client Credentials Flow).
    """
    url = f"{BASE_API_URL}/identity/v1/oauth2/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "client_credentials",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE
    }
    response = requests.post(url, headers=headers, data=data,
                             auth=(CLIENT_ID, CLIENT_SECRET))
    response.raise_for_status()
    token = response.json()["access_token"]

    session = requests.Session()
    session.headers.update({"Authorization": f"Bearer {token}"})
    return session
