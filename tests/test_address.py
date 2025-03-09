import allure
from helpers.pages.main_page import MainPage
from helpers.data_provider import DataProvider


class TestAddress:
    main_page = MainPage()

    @allure.title('Тест на проверку выбора адресса')
    def test_selection_address(self):
        param = DataProvider.get(name='address', partition='selection_existing_address')

        self.main_page.open()
        self.main_page.address_selection_with_default_city(city=param['city'], address=param['address'])
        self.main_page.assert_selected_address(param['address'])
