from model import UserInfo
from useful_methods.data_conversion import full_date_to_short


class TabUserBaseInfo:

    def __init__(self, app):
        self._app = app
        self._elements = Elements(self._app)

    def verify_user_base_info(self, user):
        email = self._elements.find_element_by_name('Эл. почта').text
        phone_number = self._elements.find_element_by_name('Телефон').text
        birth_date = self._elements.find_element_by_name('Дата рождения').text

        actual_user_info = UserInfo(
            last_name=self._elements.find_element_by_name('Фамилия').text,
            first_name=self._elements.find_element_by_name('Имя').text,
            additional_name=self._elements.find_element_by_name('Отчество').text,
            last_name_eng=self._elements.find_element_by_name('Фамилия (англ.)').text,
            first_name_eng=self._elements.find_element_by_name('Имя (англ.)').text,
            additional_name_eng=self._elements.find_element_by_name('Отчество (англ.)').text,
            birthdate=full_date_to_short(birth_date),
            account_name=self._elements.find_element_by_name('Логин в inRights').text,
            phone_number=None if phone_number == "-" else phone_number,
            email=None if email == "-" else email,
        )
        assert actual_user_info == user.info


class Elements:
    def __init__(self, app):
        self._app = app

    def find_element_by_name(self, name: str):
        xpath_row = f"""//td[.//*[text() = '{name}']]"""
        xpath_field = """//*[contains(@class, 'x-form-display-field-default')]"""
        return self._app.driver.find_element_by_xpath(xpath_row + xpath_field)
