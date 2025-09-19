import allure
from selene import browser, have, be
from selenium.common import TimeoutException


browser.config.timeout = 20


class MainPage:

    def __init__(self):
        # Хедер
        self.daily_deals_link = browser.element('//a[@aria-label="Daily Deals"]')
        self.help_contact_link = browser.element('//a[@aria-label="Help & Contact"]')
        self.sign_in_button = browser.element('//a[normalize-space()="Sign in"]')

        # Поисковая строка
        self.search_input = browser.element('//input[@id="gh-ac"]')
        self.search_button = browser.element('//span[@class="gh-search-button__label"]')

        # Результаты поиска
        self.search_results = browser.all('li.s-item .s-item__title')
        self.first_item = browser.element('li.s-item:not(.s-item--ad) a.s-item__link')

        # Фильтры
        self.condition_filter_section = browser.element('div[aria-label="Condition"]')
        self.brand_filter_section = browser.element('div[aria-label="Brand"]')
        self.price_from_input = browser.element('//input[@aria-label="Minimum Value in $"]')
        self.price_to_input = browser.element('//input[@aria-label="Maximum Value in $"]')
        self.price_submit_button = browser.element('//button[contains(@aria-label,"Submit price range")]')

        # Карточка товара
        self.item_title_detail = browser.element('#itemTitle')
        self.item_price_detail = browser.element('.notranslate')
        self.item_quantity_info = browser.element('#qtySubTxt')

        # Корзина
        self.add_to_cart_button = browser.element('#isCartBtn_btn, #atcRedesignId_btn')
        self.cart_icon = browser.element('#gh-cart-n')
        self.cart_link = browser.element('#gh-cart-i')

        # Футер
        self.footer_logo = browser.element('footer .gh-w')
        self.footer_links = browser.all('footer a')

        # Основные блоки на главной странице
        self.main_blocks = {
            "Buy": browser.all('//a[normalize-space()="Buy"]'),
            "Sell": browser.all('//a[normalize-space()="Sell"]'),
            "About eBay": browser.all('//a[normalize-space()="About eBay"]'),
            "Help & Contact": browser.all('//a[normalize-space()="Help & Contact"]')
        }

    # ---------------------- Действия ----------------------

    @allure.step("Открыть главную страницу eBay")
    def open_ebay_main_page(self):
        browser.open('/')
        return self

    @allure.step("Выполнить поиск по ключевому слову: {keyword}")
    def search_for(self, keyword):
        self.search_input.should(be.visible).type(keyword)
        self.search_button.should(be.visible).click()
        return self

    @allure.step("Применить фильтр состояния: {condition}")
    def apply_condition_filter(self, condition):
        condition_button = browser.element("//span[contains(text(),'Condition')]")
        condition_button.should(be.visible).click()

        browser.element(f"//span[normalize-space()='{condition}']").should(be.visible).click()
        return self

    @allure.step("Применить фильтр бренда: {brand}")
    def apply_brand_filter(self, brand):
        limited_brand = browser.all(f"//span[normalize-space()='{brand}']")
        if limited_brand:
            limited_brand.first.should(be.visible).click()
            return self

        see_all_button = browser.all("//button[normalize-space()='See all']")
        if see_all_button:
            see_all_button.first.should(be.visible).click()
            full_brand = browser.element(
                f"//div[contains(@class,'x-refine__multi-select')]//span[normalize-space()='{brand}']")
            full_brand.should(be.visible).click()

        return self

    @allure.step("Применить фильтр по цене от {price_from} до {price_to}")
    def apply_price_filter(self, price_from, price_to):
        self.price_from_input.should(be.visible).type(price_from)
        self.price_to_input.should(be.visible).type(price_to)
        self.price_submit_button.should(be.visible).click()
        return self

    @allure.step("Открыть первый товар из результатов поиска")
    def open_first_item(self):
        self.first_item.should(be.visible).click()
        return self

    @allure.step("Добавить товар в корзину")
    def add_to_cart(self):
        self.add_to_cart_button.should(be.visible).click()
        return self

    @allure.step("Перейти в корзину")
    def go_to_cart(self):
        self.cart_link.should(be.visible).click()
        return self

    @allure.step("Принять cookies, если баннер виден")
    def accept_cookies_if_present(self):
        try:
            browser.all("//button[normalize-space()='Accept All']").with_(timeout=5).first.should(be.visible).click()
        except TimeoutException:
            pass
        return self

    # ---------------------- Проверки ----------------------

    @allure.step("Проверить, что корзина не пуста")
    def cart_should_not_be_empty(self):
        self.cart_icon.should(be.visible).should(have.no.text('0'))
        return self

    @allure.step("Проверить элементы хэдера")
    def check_header_elements(self):
        self.daily_deals_link.should(be.visible)
        self.help_contact_link.should(be.visible)
        self.sign_in_button.should(be.visible)
        return self

    @allure.step("Проверить элементы футера")
    def check_footer_elements(self):
        self.footer_logo.should(be.visible)
        self.footer_links.should(have.size_greater_than(5))
        return self

    @allure.step("Проверить элементы карточки товара")
    def check_product_detail_elements(self):
        self.item_title_detail.should(be.visible)
        self.item_price_detail.should(be.visible)
        self.item_quantity_info.should(be.visible)
        return self

    @allure.step("Проверить наличие фильтров состояния и бренда")
    def check_condition_and_brand_filters(self):
        self.condition_filter_section.should(be.visible)
        self.brand_filter_section.should(be.visible)
        return self

    @allure.step("Проверить видимость блока '{block_name}' на главной странице")
    def check_block_visible(self, block_name: str):
        elements = self.main_blocks.get(block_name)
        if not elements:
            raise ValueError(f"No XPath defined for block '{block_name}'")
        elements.first.should(be.visible)
        return self

    @allure.step("Проверить, что есть результаты поиска")
    def should_have_results(self):
        self.search_results.should(have.size_greater_than(0))
        return self

    @allure.step("Проверить, что результаты поиска содержат текст: {text}")
    def results_should_contain(self, text):
        self.search_results.first.should(have.text(text))
        return self

    @allure.step("Проверить, что фильтр состояния применился: {condition}")
    def should_have_condition(self, condition):
        browser.element("//span[contains(@class,'x-refine__selected')]").should(have.text(condition))
        return self

    @allure.step("Проверить, что фильтр бренда применился: {brand}")
    def should_have_brand(self, brand):
        browser.element("//span[contains(@class,'x-refine__selected')]").should(have.text(brand))
        return self
