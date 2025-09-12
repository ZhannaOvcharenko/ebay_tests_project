import allure
from allure_commons.types import Severity
from pages.main_page import MainPage

main_page = MainPage()


@allure.epic("eBay Web Tests")
@allure.feature("Search Filters")
@allure.story("Laptops Filters")
@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ZhannaOvcharenko")
@allure.suite("Фильтры поиска")
@allure.title("Проверка фильтров для Laptops")
def test_laptops_filters():
    with allure.step("Предусловия: открыть главную страницу и принять cookies"):
        main_page.open_ebay_main_page().accept_cookies_if_present()

    with allure.step("Тело теста: применить фильтры"):
        (
            main_page
            .search_for("laptop")
            .apply_condition_filter("New")
            .apply_brand_filter("Dell")
            .apply_price_filter("500", "1500")
        )


@allure.epic("eBay Web Tests")
@allure.feature("Search Filters")
@allure.story("Smartphones Filters")
@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ZhannaOvcharenko")
@allure.suite("Фильтры поиска")
@allure.title("Проверка фильтров для Smartphones")
def test_smartphones_filters():
    with allure.step("Предусловия: открыть главную страницу и принять cookies"):
        main_page.open_ebay_main_page().accept_cookies_if_present()

    with allure.step("Тело теста: применить фильтры"):
        (
            main_page
            .search_for("smartphone")
            .apply_condition_filter("Used")
            .apply_brand_filter("Apple")
            .apply_price_filter("200", "800")
        )


@allure.epic("eBay Web Tests")
@allure.feature("Search Filters")
@allure.story("Watches Filters")
@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ZhannaOvcharenko")
@allure.suite("Фильтры поиска")
@allure.title("Проверка фильтров для Watches")
def test_watches_filters():
    with allure.step("Предусловия: открыть главную страницу и принять cookies"):
        main_page.open_ebay_main_page().accept_cookies_if_present()

    with allure.step("Тело теста: применить фильтры"):
        (
            main_page
            .search_for("watch")
            .apply_condition_filter("New with tags")
            .apply_brand_filter("Casio")
            .apply_price_filter("50", "500")
        )


@allure.epic("eBay Web Tests")
@allure.feature("Search Filters")
@allure.story("Tablets Filters")
@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ZhannaOvcharenko")
@allure.suite("Фильтры поиска")
@allure.title("Проверка фильтров для Tablets")
def test_tablets_filters():
    with allure.step("Предусловия: открыть главную страницу и принять cookies"):
        main_page.open_ebay_main_page().accept_cookies_if_present()

    with allure.step("Тело теста: применить фильтры"):
        (
            main_page
            .search_for("tablet")
            .apply_condition_filter("New")
            .apply_brand_filter("Samsung")
            .apply_price_filter("100", "600")
        )


@allure.epic("eBay Web Tests")
@allure.feature("Search Filters")
@allure.story("Cameras Filters")
@allure.tag("web")
@allure.severity(Severity.NORMAL)
@allure.label("owner", "ZhannaOvcharenko")
@allure.suite("Фильтры поиска")
@allure.title("Проверка фильтров для Cameras")
def test_cameras_filters():
    with allure.step("Предусловия: открыть главную страницу и принять cookies"):
        main_page.open_ebay_main_page().accept_cookies_if_present()

    with allure.step("Тело теста: применить фильтры"):
        (
            main_page
            .search_for("camera")
            .apply_condition_filter("Used")
            .apply_brand_filter("Canon")
            .apply_price_filter("150", "1000")
        )


@allure.epic("eBay Web Tests")
@allure.feature("Main Page Blocks")
@allure.story("Главная страница")
@allure.tag("web")
@allure.severity(Severity.MINOR)
@allure.label("owner", "ZhannaOvcharenko")
@allure.suite("Главная страница")
@allure.title("Проверка видимости популярных блоков на главной странице")
def test_main_blocks_visibility():
    with allure.step("Предусловия: открыть главную страницу и принять cookies"):
        main_page.open_ebay_main_page().accept_cookies_if_present()

    with allure.step("Тело теста: проверить видимость основных блоков"):
        (
            main_page
            .check_block_visible("Buy")
            .check_block_visible("Sell")
            .check_block_visible("About eBay")
            .check_block_visible("Help & Contact")
        )
