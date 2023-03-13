from selenium.webdriver.support import expected_conditions as EC


class FormMain:
    def __init__(self, app):
        self._app = app
        self._elements = Elements(app)

    def open(self):
        self._app.driver.get(self._app.config.host + "/inrights/app/index.html#!home")
        self._app.driver.wait_data_loading()
        return self

    def is_logged_in(self):
        return self._elements.btn_logout is not None

    def is_logged_in_as(self, username: str):
        return self._elements.account_name.text == username

    def logout(self):
        self._elements.btn_logout.click()
        self._app.driver.wait_data_loading()
        self._app.wait.until(EC.title_is("Вход в систему | inRights"))

class Elements:
    def __init__(self, app):
        self._app = app

    @property
    def btn_logout(self):
        xpath = """//*[contains(@class, 'logout-button')]"""
        return self._app.driver.find_element_by_xpath(xpath, timeout=1, check=True)

    @property
    def account_name(self):
        xpath = """//*[contains(@class, 'user-button')]"""
        return self._app.driver.find_element_by_xpath(xpath)
