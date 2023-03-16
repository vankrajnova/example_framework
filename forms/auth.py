from forms.main import FormMain
from webdriver import WebElement


class FormLogin:
    def __init__(self, app):
        self._app = app
        self._form_main = FormMain(self._app)
        self._elements = Elements(app)

    def open(self):
        self._app.driver.get(self._app.config.host + "/inrights/app/index.html#!home")
        self._app.driver.find_elements_by_xpath('//title[contains(text(), "Вход в систему | inRights")]', timeout=60)
        return self

    def login_as_admin(self):
        if self._app.action_mode != 'UI':
            return
        if not self._form_main.is_logged_in():
            self.open()
        self._login('administrator', '5ecr3t')
        self._inject_hide_popups()

    def login(self, username: str, password: str, forced_logout: bool = False):
        if forced_logout:
            self._form_main.logout()
        if self._form_main.is_logged_in():
            if self._form_main.is_logged_in_as(username):
                return
            else:
                self._relogin(username, password)
        else:
            self._login(username, password)
        self._inject_hide_popups()

    def _relogin(self, username: str, password: str):
        self._form_main.logout()
        self._login(username, password)

    def _login(self, username: str, password: str):
        self._elements.login.click()
        self._elements.login.send_keys(username, step=0.01)
        self._elements.password.click()
        self._elements.password.send_keys(password, step=0.01)
        self._elements.btn_login.click()

    def _inject_hide_popups(self):
        # скрываем все всплывающие сообщения
        script = "localStorage.setItem('inrights-test-suppress-toast', true);"
        self._app.driver.execute_script(script)

class Elements:
    def __init__(self, app):
        self._app = app

    @property
    def login(self) -> WebElement:
        xpath = """//input[contains(@name, 'login')]"""
        return self._app.driver.find_element_by_xpath(xpath=xpath)

    @property
    def password(self) -> WebElement:
        xpath = """//input[contains(@name, 'password')]"""
        return self._app.driver.find_element_by_xpath(xpath=xpath)

    @property
    def btn_login(self) -> WebElement:
        xpath = "//span[contains(text(), 'Войти')]"
        return self._app.driver.find_element_by_xpath(xpath=xpath)

    @property
    def btn_logout(self):
        xpath = """//*[contains(@class, 'logout-button')]"""
        return self._app.driver.find_element_by_xpath(xpath, timeout=1, check=True)
