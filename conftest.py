import json
import os.path as op

import pytest
import datetime

from fixture.app_config import make_app_config_from_json
from fixture.application import Application
from model.action_mode import ActionMode


@pytest.fixture(scope="session")
def config_as_json(request):
    config_location = request.config.getoption("--file")
    f_path = op.join(op.dirname(op.abspath(__file__)), config_location)
    with open(f_path) as f:
        config = json.load(f)
    return config


@pytest.fixture(scope="session")
def config(request, config_as_json):
    config = make_app_config_from_json(config_as_json['config'])
    host = request.config.getoption("--host")
    if host is not None:
        config.ip = host
    # config.interactive_mode = request.config.getoption("--interactive_mode")
    return config


@pytest.fixture(scope="session")
def action_mode(request, config_as_json):
    mode = request.config.getoption("--action_mode") or config_as_json['action_mode']
    return ActionMode(mode).value


@pytest.fixture(scope="session")
def app_for_session(request, config, action_mode) -> Application:
    application = Application(config, action_mode)
    application.initialize()
    request.addfinalizer(application.destroy)
    return application


@pytest.fixture
def app(app_for_session, screenshot_on_failure) -> Application:
    print_test_info(app_for_session)
    if app_for_session.action_mode == 'UI':
        if not app_for_session.is_valid():
            app_for_session.initialize()
    return app_for_session


def print_test_info(app_for_session):
    build = app_for_session.build
    action_mode = app_for_session.action_mode
    ip = app_for_session.config.ip
    dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    browser = app_for_session.config.browser.title()

    if action_mode == 'UI':
        browser_version = app_for_session.driver.capabilities['browserVersion']
        info = f'\nТест запущен: "{dt}", сборка: "{build}", стенд: "{ip}", ' \
               f'браузер: "{browser} {browser_version}", action_mode: "{action_mode}"'
        # if remote:
        #     info += f', os: "{os}'
        print(info)
    else:
        info = f'\nТест запущен: "{dt}", сборка: "{build}", стенд: "{ip}", action_mode: "{action_mode}"'
        print(info)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture
def screenshot_on_failure(request, app_for_session, action_mode):
    def fin():
        if action_mode != 'UI':
            return
        if request.node.rep_setup.failed:
            app_for_session.save_screenshot_on_failure()
        elif request.node.rep_setup.passed:
            if request.node.rep_call.failed:
                app_for_session.save_screenshot_on_failure()
    request.addfinalizer(fin)


def pytest_addoption(parser):
    parser.addoption("--file", action="store", default="./env_config.json")
    parser.addoption("--host", action="store", default=None)
    parser.addoption("--action_mode", action="store", default=None)
    parser.addoption("--interactive_mode", action="store", default=None)
