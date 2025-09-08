import logging
from allure import step
from api.authentication_api import BASE_API_URL


def get_real_item_id(session, query="laptop", offer_index=0):
    """Возвращает itemId из Browse API для Watchlist"""
    with step("Выполнить поиск товара через Browse API"):
        url = f"{BASE_API_URL}/buy/browse/v1/item_summary/search"
        params = {"q": query, "limit": 5}
        r = session.get(url, params=params)
        r.raise_for_status()
        data = r.json()
        items = data.get("itemSummaries", [])
        if not items:
            raise RuntimeError("Нет доступных товаров для Watchlist")
        item_id = items[offer_index % len(items)]["itemId"]
    return item_id


def add_item_to_favorite(session, offer_index=0, query="laptop"):
    """POST - добавление товара в избранное (Watchlist API)"""
    item_id = get_real_item_id(session, query, offer_index)

    with step("Добавление товара в избранное"):
        url = f"{BASE_API_URL}/buy/watchlist/v1/item"
        payload = {"itemId": item_id}
        r = session.post(url, json=payload)

        if r.status_code not in [200, 201]:
            text = r.text or f"Empty response, status {r.status_code}"
            raise RuntimeError(f"Ошибка добавления в избранное: {r.status_code} {text}")

    return item_id
