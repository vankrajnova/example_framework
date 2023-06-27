import allure


@allure.title('Автотест для проверки работы docker и jenkins')
def test_docker_and_ci():
    with allure.step('Test step'):
        print('It works!')
