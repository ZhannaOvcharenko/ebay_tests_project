import allure


@allure.epic("eBay Web Tests")
@allure.feature("Cart")
@allure.story("Добавление товара в корзину")
@allure.suite("Cart")
class TestCart:

    @allure.title("Добавление товара в корзину и проверка, что корзина не пуста")
    def test_add_to_cart(self, open_main_page):
        (open_main_page
            .search_for("laptop")
            .open_first_item()
            .add_to_cart()
            .cart_should_not_be_empty())
