from selenium.webdriver.common.by import By

from model import User, UserInList
from webdriver import WebElement


class FormUserList:
    def __init__(self, app):
        self._app = app
        self._elements = Elements(app)

    def open(self):
        self._app.driver.get(self._app.config.host + "/inrights/app/index.html#!users.list")
        self._app.driver.wait_data_loading()
        return self

    def open_form_user_new(self):
        self._elements.btn_create_user.click()
        self._app.driver.find_elements_by_xpath('//title[contains(text(),"Новый пользователь")]')
        return self._app.forms.user_new

    def verify_fields(self, user: User):
        actual_user_in_list = self._elements.get_user_in_list()
        assert actual_user_in_list == user.in_list, \
            'Атрибуты пользователя в списке не соответствуют ожидаемым: \n' \
            f'expected = {user.in_list}, \n' \
            f'actual = {actual_user_in_list}'

    def find_user_by_last_name(self, last_name: str):
        self._filter_users(last_name)

    def _filter_users(self, text: str):
        self._elements.filter_users.send_keys(text, step=0.05)
        self._app.driver.wait_data_loading()  # must have
        self._elements.btn_find.click()
        self._app.driver.wait_data_loading()  # must have


class Elements:
    def __init__(self, app):
        self._app = app

    def get_user_in_list(self):
        row = self._app.driver.find_element_by_xpath('//tr[contains(@class, "x-grid-row")]')
        cells = row.find_elements(by=By.XPATH, value='.//td')

        user_in_list = UserInList(
            full_name=cells[0].find_element(by=By.XPATH, value="//*[contains(@apphash, 'users.card')]").text,
            position_name=cells[1].text,
            department_name=cells[2].text,
            status=cells[3].text,
            email=None if cells[4].text == '-' else cells[4].text
        )
        return user_in_list

    @property
    def btn_create_user(self) -> WebElement:
        xpath = """//a[.//*[contains(text(), 'Создать пользователя')]]"""
        return self._app.driver.find_element_by_xpath(xpath=xpath)

    @property
    def btn_find(self):
        xpath = """//a[.//*[contains(text(), 'Найти')]]"""
        return self._app.driver.find_element_by_xpath(xpath)

    @property
    def filter_users(self):
        xpath = """//input[contains(@class,"x-form-text-search")]"""
        return self._app.driver.find_element_by_xpath(xpath)
