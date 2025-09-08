import logging
from allure import step
from api.authentication_api import BASE_API_URL

# Для тестов используем заранее известные itemId (Production)
PROD_TEST_ITEMS = [
    "v1|1234567890|0",
    "v1|0987654321|0",
    "v1|1122334455|0",
]


def get_real_item_id(session=None, offer_index=0, query=None):
    """
    Возвращает itemId для Watchlist (Production).
    Параметры session и query сохранены для совместимости.
    """
    _ = session
    _ = query

    with step("Выбираем itemId для теста"):
        item_id = PROD_TEST_ITEMS[offer_index % len(PROD_TEST_ITEMS)]
    logging.info(f"Используем item_id={item_id} для добавления в Watchlist")
    return item_id


def add_item_to_favorite(session, offer_index=0, query=None):
    """
    POST - добавление товара в избранное (Watchlist API)
    session используется для requests.Session
    """
    item_id = get_real_item_id(session, offer_index, query)

    with step("Добавление товара в избранное"):
        url = f"{BASE_API_URL}/buy/watchlist/v1/item"
        payload = {"itemId": item_id}
        r = session.post(url, json=payload)

        if r.status_code not in [200, 201]:
            text = r.text or f"Empty response, status {r.status_code}"
            logging.error(f"Ошибка добавления в избранное: {r.status_code} {text}")
            raise RuntimeError(f"Ошибка добавления в избранное: {r.status_code} {text}")

    logging.info(f"Добавлен item_id={item_id} в Watchlist")
    return item_id
