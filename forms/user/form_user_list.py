from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

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


class Elements:
    def __init__(self, app):
        self._app = app

    @property
    def btn_create_user(self) -> WebElement:
        xpath = """//a[.//*[contains(text(), 'Создать пользователя')]]"""
        return self._app.driver.find_element_by_xpath(xpath=xpath)
