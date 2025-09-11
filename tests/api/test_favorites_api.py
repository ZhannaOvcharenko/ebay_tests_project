import json
import logging
import pytest
import allure
from jsonschema import validate
from allure_commons.types import AttachmentType, Severity

# schemas
from schemas.add_favorite_request import add_favorite_request
from schemas.add_favorite_response import add_favorite_response
from schemas.delete_favorite_request import delete_favorite_request
from schemas.delete_favorite_response import delete_favorite_response

ENDPOINT_SEARCH = "/buy/browse/v1/item_summary/search"
ENDPOINT_CART = "/buy/shoppingcart/v1/cart"  # альтернативный endpoint для sandbox


def safe_json(response):
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"empty_response": True}


@allure.epic("API Tests")
@allure.feature("Public API eBay")
class TestEbayFavoritesApi:

    # ------------------- PRODUCTION TESTS -------------------
    @staticmethod
    @pytest.mark.prod
    @allure.severity(Severity.NORMAL)
    def test_get_items_search(auth_data, base_url):
        """GET - поиск товаров (работает на prod)"""
        url = f"{base_url}{ENDPOINT_SEARCH}"
        params = {"q": "laptop", "limit": 3}

        response_get = auth_data.get(url, params=params)
        response_json_get = safe_json(response_get)

        allure.attach(json.dumps(params), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json_get, indent=4), "Response", AttachmentType.JSON)

        logging.info(f"GET {url} status={response_get.status_code}")
        assert response_get.status_code == 200
        assert "itemSummaries" in response_json_get

    # ------------------- SANDBOX / ALTERNATIVE SCOPE -------------------
    @staticmethod
    @pytest.mark.sandbox
    @allure.severity(Severity.NORMAL)
    def test_post_add_cart(auth_data, base_url):
        """POST - добавление товара в корзину вместо Watchlist"""
        # Получаем первый itemId через Browse API
        search_url = f"{base_url}{ENDPOINT_SEARCH}"
        params = {"q": "laptop", "limit": 1}
        response_search = auth_data.get(search_url, params=params)
        response_search.raise_for_status()
        items = response_search.json().get("itemSummaries", [])
        assert items, "Нет товаров для добавления"
        item_id = items[0]["itemId"]

        payload_add = {"itemId": item_id}
        response_post = auth_data.post(f"{base_url}{ENDPOINT_CART}", json=payload_add)
        response_json_post = safe_json(response_post)

        allure.attach(json.dumps(payload_add), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json_post, indent=4), "Response", AttachmentType.JSON)

        logging.info(f"POST {ENDPOINT_CART} status={response_post.status_code}")

        validate(payload_add, add_favorite_request)
        if response_post.status_code in [200, 201]:
            validate(response_json_post, add_favorite_response)

        assert response_post.status_code in [200, 201]

    @staticmethod
    @pytest.mark.sandbox
    @pytest.mark.parametrize("offer_index", [0, 1])
    @allure.severity(Severity.NORMAL)
    def test_delete_cart(auth_data, base_url, offer_index):
        """DELETE - удаление товара из корзины вместо Watchlist"""
        # Получаем itemId для удаления
        search_url = f"{base_url}{ENDPOINT_SEARCH}"
        params = {"q": "laptop", "limit": offer_index + 1}
        response_search = auth_data.get(search_url, params=params)
        response_search.raise_for_status()
        items = response_search.json().get("itemSummaries", [])
        assert len(items) > offer_index, "Нет товара для удаления"
        item_id = items[offer_index]["itemId"]

        # Добавляем товар
        payload_add = {"itemId": item_id}
        response_add = auth_data.post(f"{base_url}{ENDPOINT_CART}", json=payload_add)
        response_add.raise_for_status()

        # DELETE
        url_delete = f"{base_url}{ENDPOINT_CART}/{item_id}"
        response_delete = auth_data.delete(url_delete)
        response_json_delete = safe_json(response_delete)

        allure.attach(json.dumps(payload_add), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json_delete, indent=4), "Response", AttachmentType.JSON)

        logging.info(f"DELETE {url_delete} status={response_delete.status_code}")

        validate(payload_add, delete_favorite_request)
        if response_delete.status_code == 200:
            validate(response_json_delete, delete_favorite_response)

        assert response_delete.status_code == 200

    @staticmethod
    @pytest.mark.sandbox
    @allure.severity(Severity.NORMAL)
    def test_delete_nonexistent_cart(auth_data, base_url):
        """DELETE - удаление несуществующего товара"""
        url_delete = f"{base_url}{ENDPOINT_CART}/999999999999"
        response_delete = auth_data.delete(url_delete)
        response_json_delete = safe_json(response_delete)

        allure.attach(json.dumps({"itemId": "999999999999"}), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json_delete, indent=4), "Response", AttachmentType.JSON)

        logging.info(f"DELETE {url_delete} nonexistent status={response_delete.status_code}")
        assert response_delete.status_code in [400, 404]
