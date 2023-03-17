from forms.user.tab_base_info import TabUserBaseInfo
from model import User


class FormUserCard:
    def __init__(self, app):
        self._app = app
        self._elements = Elements(app)

    def open(self, user: User):
        url_left = '/inrights/app/index.html#!users.card/{"cardId":"'
        url_right = '","tab":"info"}'
        self._app.driver.get(self._app.config.host + url_left + user.info.oid + url_right)
        self._app.driver.wait_data_loading()
        return self

    def open_tab_base_info(self) -> TabUserBaseInfo:
        self._elements.link_to_tab_base_info.click()
        return TabUserBaseInfo(self._app)


class Elements:
    def __init__(self, app):
        self._app = app

    @property
    def link_to_tab_base_info(self):
        xpath = """//*[contains(@class, 'x-tab-inner') and contains(text(), 'Информация о сотруднике')]"""
        return self._app.driver.find_element_by_xpath(xpath)
