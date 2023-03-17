import allure
import pytest
from model.user import User


@pytest.fixture
def user(base_fixture):
    return User(position=base_fixture.position_01)


@pytest.mark.test_can_use_hr
@allure.feature('Управление пользователями')
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


@pytest.mark.test_can_use_hr
@allure.feature('Управление пользователями')
@allure.story('Создание пользователя без заявки')
@allure.title('Создать пользователя. Проверки пользователя в списке пользователей')
def test_create_user_and_verify_ad_account(app, user):
    """
    Создать пользователя в inRights
    Проверить в inRights:
    Атрибуты пользователя на форме "Список пользователей"
    """
    user = app.steps.user.create_user(user)

    app.steps.user.verify_user_in_user_list(user)


@pytest.mark.test_can_use_hr
@allure.feature('Управление пользователями')
@allure.story('Создание пользователя без заявки')
@allure.title('Создать пользователя. Проверки вкладки "Информация о сотруднике"')
def test_create_user_verify_tab_base_info(app, user):
    """
    Создать пользователя
    Проверить в inRights:
    Атрибуты пользователя на вкладке "Основная информация"
    """
    user = app.steps.user.create_user(user)

    app.steps.user.verify_user_base_info(user)
