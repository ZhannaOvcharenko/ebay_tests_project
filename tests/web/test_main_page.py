import allure


@allure.epic("eBay Web Tests")
@allure.feature("Main Page")
@allure.story("Главная страница")
@allure.suite("Main Page")
class TestMainPage:

    @allure.title("Проверка видимости популярных блоков на главной странице")
    def test_main_blocks_visibility(self, open_main_page):
        (open_main_page
            .check_block_visible("Buy")
            .check_block_visible("Sell")
            .check_block_visible("About eBay")
            .check_block_visible("Help & Contact"))

    @allure.title("Проверка элементов хэдера и футера")
    def test_header_and_footer(self, open_main_page):
        (open_main_page
            .check_header_elements()
            .check_footer_elements())
