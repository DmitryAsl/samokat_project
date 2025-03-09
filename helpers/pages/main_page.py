import time
from selene import browser, have, be, query
from selenium.webdriver.common.keys import Keys
import allure


class MainPage:

    @allure.step(f"Открываем сайт")
    def open(self):
        browser.open('/')

    @allure.step("Выбираем адрес с городом по-умолчанию")
    def address_selection_with_default_city(self, city, address):
        browser.element('[class*=EmptyAddressPlug_badgeWrapper]').with_(timeout=browser.config.timeout * 2).should(
            be.visible)
        default_city = browser.element('[class*="AddressConfirmBadge_header"]>[class*="Text_text"]').get(query.text)
        assert city in default_city, f'Некорректно выбран город по умолчанию: {default_city}, ожидался: {city}'

        self.__click_button_by_text('Да, верно')
        self.__click_button_by_text('Выбрать адрес')
        self.__get_city_input_field().should(be.visible).should(have.value(city))

        self.__get_street_house_input_field().type(address)
        self.__choice_value_from_list_of_locations(address)
        self.__click_button_by_text('Да, всё верно')

    @allure.step("Выбираем продукт")
    def search_product(self, product_name):
        self.__search_field().send_keys(Keys.CONTROL + 'a' + Keys.DELETE)
        self.__search_field().type(product_name).press_enter()
        # старый элемент главной страницы долго убирается из DOM дерева
        browser.element('[class*="ProductSlider_slider"]').should(be.not_.visible)

    @allure.step("Добавляем продукт в корзину по названию")
    def add_product_to_cart_by_name(self, product_name):
        result = self.__get_productlist_details().should(have.size_greater_than(0))
        product_cart = result.element_by(have.text(product_name))
        product_cart.element(
            './/ancestor::div[contains(@class, "ProductCard_content")]//div[contains(@class, "ProductCardActions_increase")]').click()

    @allure.step("Добавляем первый продукт в корзину из результатов поиска")
    def add_first_product_from_search_to_cart(self):
        result = self.__get_productlist_details().should(have.size_greater_than(0))
        result.first.element(
            './/ancestor::div[contains(@class, "ProductCard_content")]//div[contains(@class, "ProductCardActions_increase")]').click()

    @allure.step("Увеличиваем количество конкретного товара в корзине")
    def product_quantity_increase_from_cart(self):
        browser.element('[class*="CartItemActions_root"] path[fill-rule="evenodd"]').click()

    @allure.step("Очищаем корзину")
    def clear_cart(self):
        items = self.__get_products_from_cart()
        for item in items:
            item.element('[class*="ProductItem_cross"]>svg').click()
        self.assert_empty_cart()
        # пришлось поставить т.к. не всегда успевает удалять товары
        time.sleep(1)

    @allure.step("Удаляем продукт из корзины")
    def remove_product_from_cart(self, product_name):
        product = self.__get_products_from_cart().element_by(have.text(product_name))
        product.element('[class*="ProductItem_cross"]>svg').click()

    @allure.step("Подсчитываем стоимость всей корзины")
    def calculate_cost_of_cart(self) -> int:
        products = self.__get_products_from_cart()
        cost = 0
        for product in products:
            price_text = product.element('[class*="ItemPrice_root"] span[style]').get(query.text)
            price = int(price_text.split(' ')[0])
            cost += price
        return cost

    def check_selected_address(self):
        return self.__get_selected_address().should()

    @allure.step("Проверяем результат добавление товара в корзины")
    def assert_result_addition_product_to_cart(self, product_name):
        assert len(self.__get_products_from_cart().filtered_by(have.text(product_name))) > 0

    @allure.step("Проверяем правильность расчета стоимости корзины")
    def assert_total_cost_by_cart(self):
        assert self.calculate_cost_of_cart() == self.__get_total_cart_from_page(), \
            f'Сумма цен товаров в корзине: {self.calculate_cost_of_cart()} отличается от суммы, отображаемой на странице: {self.__get_total_cart_from_page()}'

    @allure.step("Проверяем результат поиска товара")
    def assert_result_search(self, product_name: str = '', positive=True):
        if positive:
            result = self.__get_productlist_details().should(have.size_greater_than(0))
            for product in result:
                title = product.get(query.text)
                assert product_name.lower() in title.lower(), f'Название товара - {title}; не соответствует поисковой строке: {product_name}'
        else:
            header = browser.element('[class*="EmptySearchResults_root"]').should(be.visible).get(query.text)
            assert header == f'Ничего такого не нашлось', f'Некорректный текст неуспешного поиска - {header}'

    @allure.step("Проверяем, что корзина пуста")
    def assert_empty_cart(self):
        browser.element('[class*="CartPreview_cartGreeting"]').should(be.visible)

    @allure.step("Проверяем корректность выбора адреса")
    def assert_selected_address(self, address):
        address_text = self.__get_selected_address().get(query.text).replace('\n', '')
        assert address == address_text, \
            f'Указан некорректный адрес: "{address_text}", ожидался "{address}"'

    @allure.step("Проверяем корректность количества товара в корзине")
    def should_have_cart_items_count(self, count):
        assert count == len(
            self.__get_products_from_cart()), f' Некорректное количество товара в корзине - {len(self.__get_products_from_cart())}, ожидалось {count}'

    @allure.step("Проверяем корректность количества конкретного товара в корзине")
    def should_have_product_quantity_in_cart(self, count):
        product_quantity = browser.element('[class*="CartItemActions_root"] [class*= "Text_text"]').get(query.text)
        assert count == int(product_quantity)

    def __get_selected_address(self):
        return browser.element('[class*="CartHeader_address_clickable"]')

    def __click_button_by_text(self, button_text):
        browser.all('[class*=Button_control]').element_by(have.text(button_text)).click()

    def __get_city_input_field(self):
        return browser.all('input[class*="RoundedInput_input"]')[0]

    def __get_street_house_input_field(self):
        return browser.all('input[class*="RoundedInput_input"]')[1]

    def __choice_value_from_list_of_locations(self, value):
        browser.all('[class*=Suggest_suggestItem] [class*="Text_text"]').element_by(have.text(value)).should(
            be.visible).click()

    def __get_total_cart_from_page(self) -> int:
        total_text = browser.element('[class*="OrderPrice_root__UjeY1"]>span>span').should(be.visible).get(query.text)
        return int(total_text.split(' ')[0])

    def __get_products_from_cart(self):
        return browser.all('[class*="ProductItem_root"]')

    def __get_productlist_details(self):
        return browser.all('[class*="ProductsList_productList"] > a [class*="ProductCard_details"]')

    def __search_field(self):
        return browser.element('[class*=SearchInput_input]')
