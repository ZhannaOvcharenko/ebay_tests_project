import logging
import allure

BASE_API_URL = "https://api.ebay.com"
ENDPOINT_WATCHLIST = "/buy/watchlist/v1/item"


def get_real_item_id(session, offer_index=0, query="iphone"):
    """
    Получение реального itemId через Browse API.
    """
    url = f"{BASE_API_URL}/buy/browse/v1/item_summary/search"
    params = {"q": query, "limit": 3}
    r = session.get(url, params=params)
    r.raise_for_status()

    items = r.json().get("itemSummaries", [])
    if not items:
        raise RuntimeError("Не удалось найти товары по запросу")

    return items[offer_index]["itemId"]


def add_item_to_favorite(session, offer_index=0, query="iphone"):
    """
    POST - добавление товара в избранное (Watchlist API).
    """
    item_id = get_real_item_id(session, offer_index, query)

    with allure.step("Добавление товара в избранное"):
        url = f"{BASE_API_URL}{ENDPOINT_WATCHLIST}"
        payload = {"itemId": item_id}
        r = session.post(url, json=payload)

        if r.status_code not in [200, 201]:
            text = r.text or f"Empty response, status {r.status_code}"
            logging.error(f"Ошибка добавления в избранное: {r.status_code} {text}")
            raise RuntimeError(f"Ошибка добавления в избранное: {r.status_code} {text}")

        logging.info(f"Добавлен товар {item_id} в избранное (status={r.status_code})")
        return item_id
