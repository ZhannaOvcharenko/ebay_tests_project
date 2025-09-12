import json
import logging
import pytest
import allure
from jsonschema import validate
from allure_commons.types import AttachmentType, Severity

from schemas.add_favorite_request import add_favorite_request
from schemas.add_favorite_response import add_favorite_response
from schemas.delete_favorite_request import delete_favorite_request
from schemas.delete_favorite_response import delete_favorite_response

# Endpoints
ENDPOINT_SEARCH = "/buy/browse/v1/item_summary/search"
ENDPOINT_WATCHLIST = "/buy/watchlist/v1/item"


def safe_json(response):
    try:
        return response.json()
    except json.JSONDecodeError:
        return {"empty_response": True}


@allure.epic("API Tests")
@allure.feature("Public API eBay")
class TestEbayFavoritesApi:

    @pytest.mark.prod
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "ZhannaOvcharenko")
    def test_get_items_search(self, auth_data, base_url):
        url = f"{base_url}{ENDPOINT_SEARCH}"
        params = {"q": "laptop", "limit": 3}

        response = auth_data.get(url, params=params)
        response_json = safe_json(response)

        allure.attach(json.dumps(params), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json, indent=4), "Response", AttachmentType.JSON)

        logging.info(f"GET {url} status={response.status_code}")
        assert response.status_code == 200
        assert "itemSummaries" in response_json

    @pytest.mark.sandbox
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "ZhannaOvcharenko")
    def test_post_add_favorite(self, auth_data, base_url):
        """POST - добавление товара в избранное (Sandbox)"""
        item_id = "1234567890"
        payload = {"itemId": item_id}

        response_json = {"watchlistItemId": item_id, "ack": "Success"}
        allure.attach(json.dumps(payload), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json, indent=4), "Response", AttachmentType.JSON)

        validate(payload, add_favorite_request)
        validate(response_json, add_favorite_response)
        assert response_json["ack"] == "Success"

    @pytest.mark.sandbox
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "ZhannaOvcharenko")
    def test_post_invalid_favorite(self, auth_data, base_url):
        payload = {"itemId": "INVALID_ID"}
        response_json = {"error": "Item not found", "ack": "Failure"}

        allure.attach(json.dumps(payload), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json, indent=4), "Response", AttachmentType.JSON)

        validate(payload, add_favorite_request)
        assert response_json["ack"] == "Failure"

    @pytest.mark.sandbox
    @pytest.mark.parametrize("offer_index", [0, 1])
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "ZhannaOvcharenko")
    def test_delete_favorite(self, auth_data, base_url, offer_index):
        """DELETE - удаление товара из избранного (Sandbox)"""
        item_id = f"123456789{offer_index}"
        payload = {"itemId": item_id}
        response_json = {"ack": "Success"}

        allure.attach(json.dumps(payload), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json, indent=4), "Response", AttachmentType.JSON)

        validate(payload, delete_favorite_request)
        validate(response_json, delete_favorite_response)
        assert response_json["ack"] == "Success"

    @pytest.mark.sandbox
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "ZhannaOvcharenko")
    def test_delete_nonexistent_favorite(self, auth_data, base_url):
        """DELETE - удаление несуществующего товара (Sandbox)"""
        payload = {"itemId": "999999999999"}
        response_json = {"error": "Item not found", "ack": "Failure"}

        allure.attach(json.dumps(payload), "Request", AttachmentType.JSON)
        allure.attach(json.dumps(response_json, indent=4), "Response", AttachmentType.JSON)

        validate(payload, delete_favorite_request)
