import allure


@allure.title('Автотест для проверки работы docker и github actions')
def test_docker_and_ci():
    with allure.step('Test step'):
        print('It works!')
