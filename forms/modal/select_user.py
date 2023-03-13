class ModalSelectUser:
    def __init__(self, app):
        self._app = app
        self._elements = Elements(app)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ready()

    def select_user(self, user_full_name: str):
        self._find_user(user_full_name)
        self._select_user_checkbox()
        self._ready()

    def _find_user(self, user_full_name: str):
        self._elements.search_field.send_keys(user_full_name, step=.05)
        self._app.driver.wait_data_loading()  # must have

    def _select_user_checkbox(self):
        self._elements.checkbox_for_first_user.click()

    def _ready(self):
        """Жмем на кнопку готово"""
        self._elements.btn_ready.click()


class Elements:
    def __init__(self, app):
        self._app = app
        self.window_xpath = "//div[contains(@id, 'view_common_window_userSelectWindow')]"

    @property
    def search_field(self):
        xpath = """//input[contains(@class, 'x-form-text-search')]"""
        return self._app.driver.find_element_by_xpath(self.window_xpath + xpath)

    @property
    def checkbox_for_first_user(self):
        xpath = """//td[contains(@data-columnid, "checkcolumn")]"""
        return self._app.driver.find_element_by_xpath(xpath)

    @property
    def btn_ready(self):
        xpath = """//a[.//*[contains(text(), 'Готово')]]"""
        return self._app.driver.find_element_by_xpath(self.window_xpath + xpath)
