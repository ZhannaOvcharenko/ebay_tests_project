import json
import logging
import os
import allure
import pytest
from allure_commons._allure import step
from allure_commons.types import AttachmentType, Severity
from dotenv import load_dotenv
from jsonschema import validate
from api.add_favorite_api import get_item_data, add_item_to_favorite
from schemas.add_favorite_request import add_favorite_request
from schemas.add_favorite_response import add_favorite_response
from schemas.delete_favorite_request import delete_favorite_request
from schemas.delete_favorite_response import delete_favorite_response

load_dotenv()
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.mock-ebay.com")


@allure.epic("API Tests")
@allure.feature("Избранные товары")
@allure.story("Проверки для api избранных товаров")
class TestFavoritesApi:

    @allure.tag("api")
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "ZhannaOvcharenko")
    def test_success_add_favorite(self, auth_data):
        item_id, category = get_item_data(auth_data)

        fav_payload = {
            "entityId": item_id,
            "dealType": "buy",
            "entityType": category,
            "addToFolder": True
        }

        logging.info(f"POST /favorites/add payload={fav_payload}")
        validate(fav_payload, add_favorite_request)

        fav_url = f"{BASE_API_URL}/favorites/add"
        r = auth_data.post(fav_url, json=fav_payload)

        logging.info(f"Response: status={r.status_code} url={r.url}")
        allure.attach(json.dumps(fav_payload, indent=4, ensure_ascii=False),
                      name="Request Payload", attachment_type=AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4, ensure_ascii=False),
                      name="Response Body", attachment_type=AttachmentType.JSON)

        resp_json = r.json()
        assert r.status_code == 200
        assert resp_json["isAdded"] is True
        validate(resp_json, add_favorite_response)

    def test_unsuccess_add_favorite(self, auth_data):
        _, category = get_item_data(auth_data)

        fav_payload = {
            "entityId": None,
            "dealType": "buy",
            "entityType": category,
            "addToFolder": True
        }

        logging.info(f"POST /favorites/add payload={fav_payload}")
        validate(fav_payload, add_favorite_request)

        fav_url = f"{BASE_API_URL}/favorites/add"
        r = auth_data.post(fav_url, json=fav_payload)

        allure.attach(json.dumps(r.json(), indent=4, ensure_ascii=False),
                      name="Response Body", attachment_type=AttachmentType.JSON)

        assert r.status_code == 400

    @pytest.mark.parametrize("offer_index", [0, 1])
    def test_success_delete_favorite(self, auth_data, offer_index):
        item_id, category = add_item_to_favorite(auth_data, offer_index)

        fav_payload = {
            "entities": [
                {"entityIds": [item_id], "entityType": category}
            ]
        }

        logging.info(f"POST /favorites/delete payload={fav_payload}")
        validate(fav_payload, delete_favorite_request)

        fav_url = f"{BASE_API_URL}/favorites/delete"
        r = auth_data.post(fav_url, json=fav_payload)

        allure.attach(json.dumps(r.json(), indent=4, ensure_ascii=False),
                      name="Response Body", attachment_type=AttachmentType.JSON)

        resp_json = r.json()
        assert r.status_code == 200
        assert resp_json["isDeleted"] is True
        validate(resp_json, delete_favorite_response)

    def test_unsuccess_delete_favorite(self, auth_data):
        fav_payload = {
            "entities": [
                {"entityIds": [9999], "entityType": "fail_type"}
            ]
        }

        fav_url = f"{BASE_API_URL}/favorites/delete"
        r = auth_data.post(fav_url, json=fav_payload)

        assert r.status_code == 400
        resp_json = r.json()
        assert "error" in resp_json
