import allure
import pytest

from model.user import User

# @allure.title('Создать пользователя. AD: создан аккаунт и он НЕ заблокирован')
# todo: @allure.title('Создать пользователя. Пользователь корректно отображается на форме "Список пользователей"')
# todo: @allure.title('Создать пользователя. Вкладка "Основная информация" содержит корректные данные')
# todo: @allure.title('Создать пользователя. Проверки пользователя в списке пользователей')


@pytest.fixture
def user(base_fixture):
    return User(position=base_fixture.position_01)


@pytest.mark.test_can_use_hr
@allure.epic('Управление пользователями')
@allure.story('Создание пользователя без заявки')
@allure.title('Создать пользователя. Проверки в AD: УЗ создана и активна')
def test_create_user_and_verify_ad_account(app, user):
    """
    Создать пользователя в inRights
    Проверить в AD:
    1. Создана УЗ для нового пользователя
    2. УЗ активна
    """
    user = app.steps.user.create_user(user)

    app.steps.ad.verify_account_exists(user.info.account_name)

    app.steps.ad.verify_account_status(user.info.account_name, enabled=True)

