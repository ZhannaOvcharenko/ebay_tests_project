import json
import logging
import pytest
import allure
from jsonschema import validate
from allure_commons.types import AttachmentType, Severity

from api.add_favorite_api import get_item_data, add_item_to_favorite
from api.schemas.add_favorite_request import add_favorite_request
from api.schemas.add_favorite_response import add_favorite_response
from api.schemas.delete_favorite_request import delete_favorite_request
from api.schemas.delete_favorite_response import delete_favorite_response

ENDPOINT_SEARCH = "/buy/browse/v1/item_summary/search"
ENDPOINT_WATCHLIST = "/buy/watchlist/v1/item"

@allure.epic("API Tests")
@allure.feature("Public API eBay")
class TestEbayApi:

    @allure.severity(Severity.NORMAL)
    def test_get_items_search(self, auth_data, base_url):
        """GET - поиск товаров"""
        url = f"{base_url}{ENDPOINT_SEARCH}"
        params = {"q": "laptop", "limit": 3}

        r = auth_data.get(url, params=params)
        allure.attach(json.dumps(params), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4), "Response", AttachmentType.JSON)

        logging.info(f"GET {url} status={r.status_code}")
        assert r.status_code == 200
        data = r.json()
        assert "itemSummaries" in data

    @allure.severity(Severity.NORMAL)
    def test_post_add_favorite(self, auth_data, base_url):
        """POST - добавление товара в избранное"""
        item_id, _ = get_item_data(auth_data)
        payload = {"itemId": item_id}

        r = auth_data.post(f"{base_url}{ENDPOINT_WATCHLIST}", json=payload)
        allure.attach(json.dumps(payload), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4), "Response", AttachmentType.JSON)

        logging.info(f"POST {ENDPOINT_WATCHLIST} status={r.status_code}")
        assert r.status_code in [200, 201]
        validate(payload, add_favorite_request)
        validate(r.json(), add_favorite_response)

    @allure.severity(Severity.NORMAL)
    def test_post_invalid_favorite(self, auth_data, base_url):
        """POST - добавление невалидного товара"""
        payload = {"itemId": "INVALID_ID"}
        r = auth_data.post(f"{base_url}{ENDPOINT_WATCHLIST}", json=payload)
        allure.attach(json.dumps(payload), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4), "Response", AttachmentType.JSON)

        logging.info(f"POST {ENDPOINT_WATCHLIST} invalid status={r.status_code}")
        assert r.status_code in [400, 404]

    @pytest.mark.parametrize("offer_index", [0, 1])
    @allure.severity(Severity.NORMAL)
    def test_delete_favorite(self, auth_data, base_url, offer_index):
        """DELETE - удаление товара из избранного"""
        item_id, _ = add_item_to_favorite(auth_data, offer_index)
        url = f"{base_url}{ENDPOINT_WATCHLIST}/{item_id}"
        r = auth_data.delete(url)
        allure.attach(json.dumps({"itemId": item_id}), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4), "Response", AttachmentType.JSON)

        logging.info(f"DELETE {url} status={r.status_code}")
        assert r.status_code == 200
        validate(r.json(), delete_favorite_response)

    @allure.severity(Severity.NORMAL)
    def test_delete_nonexistent_favorite(self, auth_data, base_url):
        """DELETE - удаление несуществующего товара"""
        url = f"{base_url}{ENDPOINT_WATCHLIST}/999999999999"
        r = auth_data.delete(url)
        allure.attach(json.dumps({"itemId": "999999999999"}), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4), "Response", AttachmentType.JSON)

        logging.info(f"DELETE {url} nonexistent status={r.status_code}")
        assert r.status_code in [400, 404]