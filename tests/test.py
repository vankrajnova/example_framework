import json

import allure
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By


@allure.title('Example AT 1')
def test(app):

    if app.action_mode == "REST":
        # app.driver.get(url=fr'http://10.210.48.16:32737/inrights/app/index.html')
        print('REST')
        url_for_auth = fr'http://10.210.48.16:32737/inrights/api/auth/login?login=administrator&password=5ecr3t'
        rest_session = requests.session()
        response = rest_session.post(url=url_for_auth)

    else:
        print("UI")
        app.driver.get(url=fr'http://10.210.48.16:32737/inrights/app/index.html')

        user_name_xpath = """//input[contains(@name, 'login')]"""
        pwd_xpath = """//input[contains(@name, 'password')]"""

        for letter in app.config.admin_login:
            app.driver.find_element(by=By.XPATH, value=user_name_xpath).click()
            app.driver.find_element(by=By.XPATH, value=user_name_xpath).send_keys(letter)

        for letter in app.config.admin_pwd:
            app.driver.find_element(by=By.XPATH, value=pwd_xpath).click()
            app.driver.find_element(by=By.XPATH, value=pwd_xpath).send_keys(letter)

        with allure.step('step'):
            assert 1 == 2, 'Error'
