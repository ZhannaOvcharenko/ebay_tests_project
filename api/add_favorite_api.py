from allure import step

BASE_API_URL = "https://api.sandbox.ebay.com"

# Тестовые itemId для sandbox Watchlist
SANDBOX_ITEMS = [
    "v1|100000000001|0",
    "v1|100000000002|0",
    "v1|100000000003|0"
]


def get_item_data(session=None, offer_index=0, query=None):
    """
    Возвращает sandbox itemId для Watchlist.
    Параметры session и query игнорируются, сохранены для совместимости.
    """
    # Подавляем предупреждения об unused
    _ = session
    _ = query

    with step("Выбираем sandbox itemId"):
        item_id = SANDBOX_ITEMS[offer_index % len(SANDBOX_ITEMS)]
        category = "electronics"  # фиктивная категория
    return item_id, category


def add_item_to_favorite(session, offer_index=0, query="laptop"):
    """
    POST - добавление товара в избранное (Watchlist API)
    session используется для requests.Session
    """
    item_id, category = get_item_data(session, offer_index, query)

    with step("Добавление товара в избранное"):
        url = f"{BASE_API_URL}/buy/watchlist/v1/item"
        payload = {"itemId": item_id}
        r = session.post(url, json=payload)

        if r.status_code not in [200, 201]:
            text = r.text or f"Empty response, status {r.status_code}"
            raise RuntimeError(f"Ошибка добавления в избранное: {r.status_code} {text}")

    return item_id, category
