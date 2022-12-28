import allure
from allure_commons.types import AttachmentType

from rest.transaction import RestTransaction
from rest.version import get_build_info
from webdriver import WebDriver, webdriver_data


class Application:
    def __init__(self, config, action_mode):
        self.config = config
        self.action_mode = action_mode
        self._driver = None

    def initialize(self):
        if self.action_mode == "UI":
            self._driver = WebDriver(**webdriver_data)
            self._driver.maximize_window()

    @property
    def driver(self):
        if self.action_mode == 'UI':
            return self._driver
        else:
            raise Exception(f'Во время {self.action_mode}-прогона произошло обращение к WebDriver')

    def start_new_rest_transaction(self, transaction_name) -> RestTransaction:
        return RestTransaction(self, transaction_name)

    @property
    def build(self):
        return get_build_info(self)

    def is_valid(self):
        try:
            url = self.driver.current_url
            return True
        except:
            return False

    def destroy(self):
        if self.action_mode == 'UI':
            self.driver.quit()

    def save_screenshot_on_failure(self):
        allure.attach(body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
