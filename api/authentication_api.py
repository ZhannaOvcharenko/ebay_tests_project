import requests
import os
from dotenv import load_dotenv

load_dotenv()


def get_auth_cookie():
    base_url = os.getenv("EBAY_API_URL", "https://api.mock-ebay.com")

    session = requests.Session()
    fake_cookie = "mock-session-cookie"
    return session, fake_cookie
