import os
import random
from allure_commons._allure import step
from dotenv import load_dotenv

load_dotenv()
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.mock-ebay.com")


def get_item_data(session, offer_index=0):
    """
    Эмуляция поиска товаров на eBay
    """

    with step("Выполнить запрос на поиск товаров"):
        url = f"{BASE_API_URL}/search"
        payload = {"query": "laptop", "page": 1}
        r = session.get(url, params=payload)
        r.raise_for_status()
        data = r.json()

        items = data.get("items", [])
        if not items or not isinstance(items, list):
            raise RuntimeError("В ответе нет списка items")

    with step("Получить данные по выбранному товару"):
        item = items[offer_index]
        item_id = item.get("itemId", random.randint(1000, 9999))
        category = item.get("category", "electronics")

    return item_id, category


def add_item_to_favorite(session, offer_index=0):
    """
    Эмуляция добавления товара в избранное
    """
    item_id, category = get_item_data(session, offer_index)

    with step("Выполнить запрос на добавление товара в избранное"):
        url = f"{BASE_API_URL}/favorites/add"
        payload = {
            "entityId": item_id,
            "dealType": "buy",
            "entityType": category,
            "addToFolder": True
        }
        r = session.post(url, json=payload)
        r.raise_for_status()

    return item_id, category
