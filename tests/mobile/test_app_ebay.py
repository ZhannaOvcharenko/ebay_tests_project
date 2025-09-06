import allure


@allure.feature("Search")
@allure.story("Search for items")
def test_search_item(driver):
    with allure.step("Открыть поиск и ввести запрос 'iPhone'"):
        search_box = driver.find_element_by_accessibility_id("Search")
        search_box.click()
        search_box.send_keys("iPhone")
        driver.press_keycode(66)  # Enter

    with allure.step("Проверить, что результаты появились"):
        results = driver.find_elements_by_id("com.ebay.mobile:id/textview_item_title")
        assert len(results) > 0


@allure.feature("Login")
@allure.story("Successful login")
def test_login_success(driver):
    with allure.step("Открыть экран входа"):
        driver.find_element_by_accessibility_id("Sign in").click()

    with allure.step("Ввести данные из .env.bstack"):
        driver.find_element_by_id("com.ebay.mobile:id/edit_text_username").send_keys("test_user")
        driver.find_element_by_id("com.ebay.mobile:id/edit_text_password").send_keys("correct_password")
        driver.find_element_by_id("com.ebay.mobile:id/button_sign_in").click()

    with allure.step("Проверить успешный вход"):
        assert driver.find_element_by_accessibility_id("My eBay").is_displayed()


@allure.feature("Login")
@allure.story("Invalid password")
def test_login_invalid_password(driver):
    with allure.step("Открыть экран входа"):
        driver.find_element_by_accessibility_id("Sign in").click()

    with allure.step("Ввести неверный пароль"):
        driver.find_element_by_id("com.ebay.mobile:id/edit_text_username").send_keys("test_user")
        driver.find_element_by_id("com.ebay.mobile:id/edit_text_password").send_keys("wrong_password")
        driver.find_element_by_id("com.ebay.mobile:id/button_sign_in").click()

    with allure.step("Проверить сообщение об ошибке"):
        error = driver.find_element_by_id("com.ebay.mobile:id/textview_error")
        assert error.is_displayed()
