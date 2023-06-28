import allure


@allure.title("Test for verify work of the docker container and CI/CD")
def test_docker_and_ci():
    with allure.step('Test step'):
        print('It works!')
