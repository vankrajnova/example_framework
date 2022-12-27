import json

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By

from root_dir_path import ROOT_DIR

# ip = '10.210.48.16'
# port = '32737'
#
# login = 'administrator'
# pwd = '5ecr3t'
#
# action_mode = 'UI'

# browser = 'chrome'
# interactive_mode = True
window_size = "window-size=1920x1080"


def _get_config():
    with open(ROOT_DIR + r"/env_config.json", "r", encoding="UTF-8") as f:
        env_config = json.load(f)
        return env_config


def test_login_by_rest():
    config = _get_config()

    # response = requests.get('http://10.210.48.16:32737/inrights/app/index.html')

    url_for_auth = fr'http://{config["config"]["ip"]}:{config["config"]["port"]}/inrights/api/auth/login?login={config["config"]["admin_login"]}&password={config["config"]["admin_pwd"]}'
    rest_session = requests.session()
    response = rest_session.post(url=url_for_auth)

    if response.status_code == 200:
        print('administrator logged')
    else:
        print('failed\n')
        print(response.json())


def test_login_by_ui():
    config = _get_config()

    if config["config"]["browser"] == 'chrome':
        options = webdriver.ChromeOptions()
        options.add_argument(window_size)
        options.capabilities['goog:loggingPrefs'] = {'performance': 'ALL'}
        if not config["config"]["interactive_mode"]:
            options.add_argument("--no-sandbox")
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--width=1920")
            options.add_argument("--height=1080")

        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(30)
        driver.maximize_window()
    else:
        raise Exception('Указан неправильный браузер')

    driver.get(url=fr'http://{config["config"]["ip"]}:{config["config"]["port"]}/inrights/app/index.html')

    user_name_xpath = """//input[contains(@name, 'login')]"""
    pwd_xpath = """//input[contains(@name, 'password')]"""

    for letter in config["config"]["admin_login"]:
        driver.find_element(by=By.XPATH, value=user_name_xpath).click()
        driver.find_element(by=By.XPATH, value=user_name_xpath).send_keys(letter)

    for letter in config["config"]["admin_pwd"]:
        driver.find_element(by=By.XPATH, value=pwd_xpath).click()
        driver.find_element(by=By.XPATH, value=pwd_xpath).send_keys(letter)

    driver.quit()



def test():
    s = 'Adm'
    print(s.lower())

