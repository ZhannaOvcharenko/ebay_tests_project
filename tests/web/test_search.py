import pytest
import allure

search_test_data = [
    ("laptop", "New", "Dell", "500", "1500"),
    ("smartphone", "Used", "Apple", "200", "800"),
    ("watch", "New with tags", "Casio", "50", "500"),
    ("tablet", "New", "Samsung", "100", "600"),
    ("camera", "Used", "Canon", "150", "1000"),
]


@allure.epic("eBay Web Tests")
@allure.feature("Search")
@allure.story("Фильтры поиска")
@allure.suite("Search")
@pytest.mark.parametrize("keyword,condition,brand,price_from,price_to", search_test_data)
def test_search_filters(open_main_page, keyword, condition, brand, price_from, price_to):
    (open_main_page
        .search_for(keyword)
        .apply_condition_filter(condition)
        .apply_brand_filter(brand)
        .apply_price_filter(price_from, price_to)
        .should_have_results()
        .should_have_condition(condition)
        .should_have_brand(brand))
