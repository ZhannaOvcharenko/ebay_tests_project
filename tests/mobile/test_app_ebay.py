import allure
from allure_commons.types import Severity
from appium.webdriver.common.appiumby import AppiumBy
from selene.support.conditions import have
from selene.support.shared import browser


@allure.epic("Mobile Tests")
@allure.feature("eBay Mobile")
@allure.story("Search and Login Tests")
class TestEbayMobile:

    @allure.tag("mobile")
    @allure.severity(Severity.NORMAL)
    @allure.label("owner", "automation_team")
    def test_search_item(self):
        with allure.step("Открыть поиск и ввести 'iPhone'"):
            browser.element((AppiumBy.ACCESSIBILITY_ID, "Search")).click()
            browser.element((AppiumBy.ACCESSIBILITY_ID, "Search")).send_keys("iPhone")
            browser.driver.press_keycode(66)  # Enter

        with allure.step("Проверить, что появились результаты"):
            results = browser.elements((AppiumBy.ID, "com.ebay.mobile:id/textview_item_title"))
            assert len(results) > 0

    @allure.tag("mobile")
    @allure.severity(Severity.CRITICAL)
    @allure.label("owner", "automation_team")
    def test_login_success(self):
        with allure.step("Открыть экран входа"):
            browser.element((AppiumBy.ACCESSIBILITY_ID, "Sign in")).click()

        with allure.step("Ввести корректные данные"):
            browser.element((AppiumBy.ID, "com.ebay.mobile:id/edit_text_username")).send_keys("test_user")
            browser.element((AppiumBy.ID, "com.ebay.mobile:id/edit_text_password")).send_keys("correct_password")
            browser.element((AppiumBy.ID, "com.ebay.mobile:id/button_sign_in")).click()

        with allure.step("Проверить успешный вход"):
            browser.element((AppiumBy.ACCESSIBILITY_ID, "My eBay")).should(have.text("My eBay"))

    @allure.tag("mobile")
    @allure.severity(Severity.CRITICAL)
    @allure.label("owner", "automation_team")
    def test_login_invalid_password(self):
        with allure.step("Открыть экран входа"):
            browser.element((AppiumBy.ACCESSIBILITY_ID, "Sign in")).click()

        with allure.step("Ввести неверный пароль"):
            browser.element((AppiumBy.ID, "com.ebay.mobile:id/edit_text_username")).send_keys("test_user")
            browser.element((AppiumBy.ID, "com.ebay.mobile:id/edit_text_password")).send_keys("wrong_password")
            browser.element((AppiumBy.ID, "com.ebay.mobile:id/button_sign_in")).click()

        with allure.step("Проверить сообщение об ошибке"):
            browser.element((AppiumBy.ID, "com.ebay.mobile:id/textview_error")).should(have.text("Incorrect password"))
