from model.unit import Position, Orgunit
from model.user import User

# @allure.title('Создать пользователя. AD: создан аккаунт и он НЕ заблокирован')
# @allure.title('Создать пользователя. Пользователь корректно отображается на форме "Список пользователей"')
# @allure.title('Создать пользователя. Вкладка "Основная информация" содержит корректные данные')

def test_1(app, base_fixture):
    user = User(position=base_fixture.position_01)

    app.steps.user.create_user(user=user)



