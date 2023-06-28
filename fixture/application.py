import allure
from allure_commons.types import AttachmentType

from forms.factory import FormFactory
from helpers.factory import HelpersFactory
from hr.hr_factory import HrFactory
from rest.factory import RestFactory
from rest.transaction import RestTransaction
from rest.version import get_build_info
from steps.factory import StepsFactory
from webdriver import WebDriver, webdriver_data


class Application:
    def __init__(self, config, db, action_mode, base_fixture):
        self.config = config
        self.action_mode = action_mode
        self.db = db
        self.base_fixture = base_fixture
        self.forms = FormFactory(self)
        self.rest = RestFactory(self)
        self.hr = HrFactory(self)
        self.steps = StepsFactory(self)
        self.helpers = HelpersFactory(self)
        self._driver = None

    def initialize(self):
        if self.action_mode == "UI":
            self._driver = WebDriver(**webdriver_data)
            self._driver.maximize_window()

    def is_valid_inrights(self):
        try:
            self.forms.auth.login_as_admin()
            return True
        except Exception as e:
            print(e)
            print('\nTimeoutException when trying to login (before running the test)')
        return False

    def reopen(self):
        try:
            self.driver.quit()
        except Exception:
            print('\nAn error occurred while trying to execute the command: "self.driver.quit()"')
        self.initialize()
        self.forms.auth.login_as_admin()

    @property
    def driver(self):
        if self.action_mode == 'UI':
            return self._driver
        else:
            raise Exception(f'WebDriver was called during {self.action_mode} action mode')

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
        self.helpers.pwsh.close()
        if self.action_mode == 'UI':
            self.driver.quit()

    def save_screenshot_on_failure(self):
        allure.attach(body=self.driver.get_screenshot_as_png(),
                      attachment_type=AttachmentType.PNG)
