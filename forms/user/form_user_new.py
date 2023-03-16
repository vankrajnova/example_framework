from forms.modal.select_unit import ModalSelectUnit
from forms.modal.select_user import ModalSelectUser
from model import User, UserInfo, Position


class FormUserNew:
    def __init__(self, app):
        self._app = app
        self._elements = Elements(app)

    def create_user(self, user: User):
        self._fill_form(user)
        self._save()
        return user

    def _fill_form(self, user: User):
        self._fill_user_info(user)
        self._fill_employment_info(user)
        self._elements.checkbox_create_request.click()

    def _fill_user_info(self, user: User):
        self._elements.find_element_by_name('lastName').send_keys(user.info.last_name)
        self._elements.find_element_by_name('firstName').send_keys(user.info.first_name)
        self._elements.find_element_by_name('additionalName').send_keys(user.info.last_name)
        self._elements.find_element_by_name('lastName_en').send_keys(user.info.last_name_eng)
        self._elements.find_element_by_name('firstName_en').send_keys(user.info.first_name_eng)
        self._elements.find_element_by_name('additionalName_en').send_keys(user.info.additional_name_eng)
        self._elements.find_element_by_name('dateOfBirth').send_keys(user.info.birthdate)

    def _fill_employment_info(self, user: User):
        self._select_hr_status(user.employment.status)
        self._select_position(user.employment.position)

        if user.employment.manager_info:
            self._select_manager(user.employment.manager_info.full_name)

        self._elements.find_element_by_name('type').send_keys(user.employment.user_type)
        self._elements.find_element_by_name('dateFrom').send_keys(user.employment.start_date)
        self._elements.find_element_by_name('region').send_keys(user.employment.region)
        self._elements.find_element_by_name('city').send_keys(user.employment.city)
        self._elements.find_element_by_name('office').send_keys(user.employment.office)
        if user.employment.contract_number:
            self._elements.find_element_by_name('contractNumber').send_keys(user.employment.contract_number)
        if user.employment.lwd:
            self._elements.find_element_by_name('lwd').send_keys(user.employment.lwd)

    def _select_position(self, position: Position):
        self._elements.btn_select_position.click()
        with ModalSelectUnit(self._app) as modal_unit:
            modal_unit.select_unit(position.name)

    def _select_manager(self, manager_info: UserInfo):
        self._elements.btn_select_manager.click()
        with ModalSelectUser(self._app) as modal_user:
            modal_user.select_user(manager_info.full_name)

    def _select_hr_status(self, hr_status: str):
        # раскрываем dropdown со списком hr статусов
        self._elements.find_element_by_name('hrStatus').click()
        self._elements.hr_status(hr_status).click()

    def _save(self):
        self._elements.btn_save.click()
        self._app.driver.wait_data_loading()


class Elements:
    def __init__(self, app):
        self._app = app

    def find_element_by_name(self, name: str):
        xpath = f"""//input[contains(@name, '{name}')]"""
        return self._app.driver.find_element_by_xpath(xpath)

    @property
    def btn_select_position(self):
        xpath = """//*[contains(@name, 'position')]"""
        return self._app.driver.find_element_by_xpath(xpath)

    @property
    def btn_select_manager(self):
        xpath = """//*[contains(@name, 'manager')]"""
        return self._app.find_element_by_xpath(xpath)

    def hr_status(self, hr_status: str):
        xpath = f"""//*[contains(@role, 'option') and contains(text(), '{hr_status}')]"""
        return self._app.driver.find_element_by_xpath(xpath)

    @property
    def checkbox_create_request(self):
        xpath = """//div[.//label[contains(text(),"Создать заявку")] and contains(@class,"x-form-type-checkbox")]"""
        return self._app.driver.find_element_by_xpath(xpath)

    @property
    def btn_save(self):
        xpath = """//a[.//*[contains(text(), 'Сохранить')]]"""
        return self._app.driver.find_element_by_xpath(xpath)

    @property
    def btn_confirm_created_request(self):
        xpath = """//span[contains(text(), 'Подтвердить')]"""
        return self._app.driver.find_element_by_xpath(xpath)
