import random
from allure import step

BASE_API_URL = "https://api.sandbox.ebay.com"


def get_item_data(session, offer_index=0, query="laptop"):
    """GET - поиск товаров через Browse API"""
    with step("Выполнить запрос на поиск товаров"):
        url = f"{BASE_API_URL}/buy/browse/v1/item_summary/search"
        params = {"q": query, "limit": 5}
        r = session.get(url, params=params)

        if r.status_code != 200:
            raise RuntimeError(f"Ошибка запроса: {r.status_code} {r.text}")

        data = r.json()
        items = data.get("itemSummaries", [])
        if not items:
            raise RuntimeError("В ответе нет itemSummaries")

    with step("Выбираем товар"):
        item = items[offer_index]
        item_id = item.get("itemId", str(random.randint(100000, 999999)))
        category = item.get("categoryPath", "electronics")

    return item_id, category


def add_item_to_favorite(session, offer_index=0, query="laptop"):
    """POST - добавление товара в избранное (Watchlist API)"""
    item_id, category = get_item_data(session, offer_index, query)

    with step("Добавление товара в избранное"):
        url = f"{BASE_API_URL}/buy/watchlist/v1/item"
        payload = {"itemId": item_id}
        r = session.post(url, json=payload)

        if r.status_code not in [200, 201]:
            raise RuntimeError(f"Ошибка добавления в избранное: {r.status_code} {r.text}")

    return item_id, category
