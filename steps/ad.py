import allure

from rest.transaction import wait


class ADSteps:

    def __init__(self, app):
        self._app = app

    @wait()
    def verify_account_exists(self, account_name):
        with allure.step(f'[AD] Проверить, что УЗ "{account_name}" есть в AD'):
            account_name_list = self._app.helpers.pwsh.get_account_name_list()
            assert account_name in account_name_list, f'УЗ {account_name} нет в AD'

    @wait()
    def verify_account_status(self, account_name, enabled: bool):
        with allure.step(
            f'[AD] Проверить, что УЗ "{account_name}" {"активна" if enabled else "заблокирована"}'
        ):
            status = self._app.helpers.pwsh.get_account_status(account_name)
            assert status == str(enabled), f'Атрибут "Enabled" в AD заполнен некорректно\n' \
                                           f'{enabled=},\n' \
                                           f'{status=}'
