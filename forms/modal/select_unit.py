from selenium.webdriver import Keys


class ModalSelectUnit:
    def __init__(self, app):
        self._app = app
        self._elements = Elements(app)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._ready()

    def select_unit(self, unit_name: str):
        self._find_unit(unit_name)
        self._select_unit_checkbox(unit_name)

    def _find_unit(self, unit_name: str):
        self._elements.search_field.click()
        self._elements.search_field.send_keys(unit_name, step=0.05)
        self._elements.search_field.send_keys(Keys.ENTER, clear=False)
        self._app.driver.wait_data_loading()  # must have

    def _select_unit_checkbox(self, unit_name: str):
        self._elements.checkbox_for_unit_by_name(unit_name).click()

    def _ready(self):
        """Жмем на кнопку готово"""
        self._elements.btn_ready.click()


class Elements:
    def __init__(self, app):
        self._app = app
        self.window_xpath = "//div[contains(@id, 'view_common_window_orgSelectWindow')]"

    @property
    def search_field(self):
        xpath = """//input[contains(@class, 'x-form-text-search')]"""
        return self._app.driver.find_element_by_xpath(self.window_xpath + xpath)

    def checkbox_for_unit_by_name(self, unit_name: str):
        unit_row_xpath = f"""//*[contains(@class, 'x-grid-row')][.//*[contains(text(), '{unit_name}')]]"""
        unit_checkbox_xpath = """//*[contains(@class, 'x-grid-checkcolumn-cell-inner')]"""
        return self._app.driver.find_element_by_xpath(unit_row_xpath + unit_checkbox_xpath)

    @property
    def btn_ready(self):
        xpath = """//a[.//*[contains(text(), 'Готово')]]"""
        return self._app.driver.find_element_by_xpath(self.window_xpath + xpath)
