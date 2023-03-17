import allure

from model import User
from useful_methods.representation import pretty_print


class UserSteps:
    def __init__(self, app):
        self._app = app

    def create_user(
            self, user: User, only_rest: bool = False, logged_in_user: User = None
    ) -> User:
        action_mode = "REST" if only_rest else self._app.action_mode

        if action_mode == "HR":
            initiator = "В кадровом источнике"
        else:
            initiator = "administrator" if not logged_in_user else f"{logged_in_user.info.account_name}"

        with allure.step(f'[{action_mode}] [{initiator}] Создать пользователя "{user.info.account_name}" '
                         f'с ТУ на должность "{user.employment.position.name}"'):

            if action_mode == 'HR':
                user = self._app.hr.user.create_user(user)
            elif action_mode == 'UI':
                if logged_in_user:
                    self._app.forms.auth.login(logged_in_user.info.account_name, logged_in_user.info.password)
                form_user_list = self._app.forms.open_form_user_list()
                form_user_new = form_user_list.open_form_user_new()
                user = form_user_new.create_user(user)
            else:
                user = self._app.rest.user.create_user(user, logged_in_user)

            user.info.oid = self._app.rest.repository.get_user_oid(user.info.last_name)

            pretty_print("Created user: ", user)
            return user

    def verify_user_in_user_list(self, user: User, logged_in_user: User = None):
        step_name = f'[{self._app.action_mode}]' \
                    f' [{"administrator" if not logged_in_user else logged_in_user.info.account_name}]' \
                    f' Проверить атрибуты пользователя' \
                    f' "{user.info.account_name}" в списке пользователей'

        with allure.step(step_name):
            if self._app.action_mode == "UI":
                if logged_in_user:
                    self._app.forms.auth.login(logged_in_user.info.account_name, logged_in_user.info.password)
                form_user_list = self._app.forms.open_form_user_list()
                form_user_list.find_user_by_last_name(user.info.last_name)
                form_user_list.verify_fields(user)
            else:
                self._app.rest.user.verify_user_in_user_list(user)

    def verify_user_base_info(self, user: User, logged_in_user: User = None):
        step_name = f'[{self._app.action_mode}] ' \
                    f'[{"administrator" if logged_in_user is None else logged_in_user.info.account_name}] ' \
                    f'Проверить данные на вкладке "Информация о сотруднике" ' \
                    f'в карточке пользователя "{user.info.account_name}"'

        with allure.step(step_name):
            if self._app.action_mode == "UI":
                if logged_in_user is not None:
                    self._app.forms.auth.login(logged_in_user.info.account_name, logged_in_user.info.password)
                user_card = self._app.forms.open_form_user_card(user)
                tab_base_info = user_card.open_tab_base_info()
                tab_base_info.verify_user_base_info(user)
            else:
                self._app.rest.user.verify_user_base_info(user)