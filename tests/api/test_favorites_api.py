import json
import logging
import os
import allure
import pytest
from allure import step
from allure_commons.types import AttachmentType, Severity
from dotenv import load_dotenv
from jsonschema import validate

from api.add_favorite_api import get_item_data, add_item_to_favorite
from schemas.add_favorite_request import add_favorite_request
from schemas.add_favorite_response import add_favorite_response
from schemas.delete_favorite_request import delete_favorite_request
from schemas.delete_favorite_response import delete_favorite_response

load_dotenv()
BASE_API_URL = os.getenv("EBAY_API_URL", "https://api.sandbox.ebay.com")


@allure.epic("API Tests")
@allure.feature("Избранные товары (Watchlist)")
@allure.story("Проверки API eBay для работы с избранным")
class TestFavoritesApi:

    @allure.tag("api")
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "ZhannaOvcharenko")
    def test_success_add_favorite(self, auth_data):
        """
        Успешное добавление товара в избранное
        """
        # Arrange
        item_id, category = get_item_data(auth_data)

        fav_payload = {"itemId": item_id}

        logging.info(f"POST /buy/watchlist/v1/item payload={fav_payload}")

        with step("Провалидировать схему запроса"):
            validate(fav_payload, add_favorite_request)

        # Act
        fav_url = f"{BASE_API_URL}/buy/watchlist/v1/item"
        r = auth_data.post(fav_url, json=fav_payload)

        # Allure attachments
        allure.attach(json.dumps(fav_payload, indent=4, ensure_ascii=False),
                      name="Request Payload", attachment_type=AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4, ensure_ascii=False),
                      name="Response Body", attachment_type=AttachmentType.JSON)

        logging.info(f"Response: status={r.status_code} url={r.url}")

        # Assert
        resp_json = r.json()
        assert r.status_code == 200
        assert resp_json["ack"].lower() in ["success", "warning"]
        validate(resp_json, add_favorite_response)

    def test_unsuccess_add_favorite(self, auth_data):
        """
        Ошибка при добавлении избранного (невалидный itemId)
        """
        # Arrange
        fav_payload = {"itemId": "INVALID_ID"}

        logging.info(f"POST /buy/watchlist/v1/item payload={fav_payload}")

        with step("Провалидировать схему запроса"):
            validate(fav_payload, add_favorite_request)

        # Act
        fav_url = f"{BASE_API_URL}/buy/watchlist/v1/item"
        r = auth_data.post(fav_url, json=fav_payload)

        allure.attach(json.dumps(fav_payload, indent=4, ensure_ascii=False),
                      name="Request Payload", attachment_type=AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4, ensure_ascii=False),
                      name="Response Body", attachment_type=AttachmentType.JSON)

        # Assert
        assert r.status_code in [400, 404]
        resp_json = r.json()
        assert "errors" in resp_json

    @pytest.mark.parametrize("offer_index", [0, 1])
    def test_success_delete_favorite(self, auth_data, offer_index):
        """
        Успешное удаление товара из избранного
        """
        # Arrange
        item_id, _ = add_item_to_favorite(auth_data, offer_index)

        fav_payload = {"itemId": item_id}

        logging.info(f"DELETE /buy/watchlist/v1/item payload={fav_payload}")

        with step("Провалидировать схему запроса"):
            validate(fav_payload, delete_favorite_request)

        # Act
        fav_url = f"{BASE_API_URL}/buy/watchlist/v1/item/{item_id}"
        r = auth_data.delete(fav_url)

        allure.attach(json.dumps(fav_payload, indent=4, ensure_ascii=False),
                      name="Request Payload", attachment_type=AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4, ensure_ascii=False),
                      name="Response Body", attachment_type=AttachmentType.JSON)

        logging.info(f"Response: status={r.status_code} url={r.url}")

        # Assert
        resp_json = r.json()
        assert r.status_code == 200
        assert resp_json["ack"].lower() in ["success", "warning"]
        validate(resp_json, delete_favorite_response)

    def test_unsuccess_delete_favorite(self, auth_data):
        """
        Ошибка при удалении (несуществующий товар)
        """
        # Arrange
        fav_payload = {"itemId": "999999999999"}

        logging.info(f"DELETE /buy/watchlist/v1/item payload={fav_payload}")

        with step("Провалидировать схему запроса"):
            validate(fav_payload, delete_favorite_request)

        # Act
        fav_url = f"{BASE_API_URL}/buy/watchlist/v1/item/999999999999"
        r = auth_data.delete(fav_url)

        allure.attach(json.dumps(fav_payload, indent=4, ensure_ascii=False),
                      name="Request Payload", attachment_type=AttachmentType.JSON)
        allure.attach(json.dumps(r.json(), indent=4, ensure_ascii=False),
                      name="Response Body", attachment_type=AttachmentType.JSON)

        # Assert
        assert r.status_code in [400, 404]
        resp_json = r.json()
        assert "errors" in resp_json
