import os
import random
from allure import step
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.sandbox.ebay.com")


def get_item_data(session, offer_index=0, query="laptop"):
    """
    Поиск товаров на eBay через Browse API
    """
    with step("Выполнить запрос на поиск товаров"):
        url = f"{BASE_API_URL}/buy/browse/v1/item_summary/search"
        params = {"q": query, "limit": 5}
        r = session.get(url, params=params)
        r.raise_for_status()
        data = r.json()

        items = data.get("itemSummaries", [])
        if not items or not isinstance(items, list):
            raise RuntimeError("В ответе нет списка itemSummaries")

    with step("Получить данные по выбранному товару"):
        item = items[offer_index]
        item_id = item.get("itemId", str(random.randint(100000, 999999)))
        category = item.get("categoryPath", "electronics")

    return item_id, category


def add_item_to_favorite(session, offer_index=0, query="laptop"):
    """
    Добавление товара в избранное (Watchlist API)
    """
    item_id, category = get_item_data(session, offer_index, query)

    with step("Выполнить запрос на добавление товара в избранное"):
        url = f"{BASE_API_URL}/buy/watchlist/v1/item"
        payload = {"itemId": item_id}
        r = session.post(url, json=payload)
        r.raise_for_status()

    return item_id, category
