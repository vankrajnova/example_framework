import json
import os.path as op

import pytest
import datetime

from fixture.app_config import make_app_config_from_json
from fixture.application import Application
from fixture.base_fixture import BaseFixture
from fixture.db_mssql import MSSQL
from fixture.db_postgresql import Postgresql
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
def db(request, config_as_json, action_mode):
    if action_mode != 'HR':
        return None
    db_config = config_as_json['db']
    if db_config['type'] == 'postgresql':
        db_fixture = Postgresql(host=db_config['host'], port=db_config['port'], name=db_config['name'],
                                user=db_config['user'], pwd=db_config['pwd'])
    else:
        db_fixture = MSSQL(host=db_config['host'], port=db_config['port'], name=db_config['name'],
                           user=db_config['user'], pwd=db_config['pwd'])
    host = request.config.getoption("--host")
    if host is not None:
        db_fixture.host = host

    def finalize():
        if action_mode.global_mode != 'HR':
            return
        db_fixture.destroy()

    request.addfinalizer(finalize)
    return db_fixture


@pytest.fixture(scope="session")
def app_for_session(request, config, db, action_mode, base_fixture) -> Application:
    application = Application(config, db, action_mode, base_fixture)
    application.initialize()
    request.addfinalizer(application.destroy)
    return application


@pytest.fixture
def app(app_for_session, screenshot_on_failure) -> Application:
    print_test_info(app_for_session)
    if app_for_session.action_mode == 'UI':
        if not app_for_session.is_valid():
            app_for_session.initialize()
        if not app_for_session.is_valid_inrights():
            app_for_session.reopen()
    return app_for_session


def print_test_info(app_for_session):
    build = app_for_session.build
    action_mode = app_for_session.action_mode
    ip = app_for_session.config.ip
    dt = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    browser = app_for_session.config.browser.title()
    # db_type = app_for_session.config.inrights_db_type.title()

    if action_mode == 'UI':
        browser_version = app_for_session.driver.capabilities['browserVersion']
        info = f'\nТест запущен: "{dt}", сборка: "{build}", стенд: "{ip}", ' \
               f'браузер: "{browser} {browser_version}", action_mode: "{action_mode}"'
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

@pytest.fixture(scope="session")
def base_fixture(config_as_json):
    db_config = config_as_json['db']
    if db_config['type'] == 'postgresql':
        return BaseFixture('postgresql')
    else:
        return BaseFixture('mssql')

def pytest_addoption(parser):
    parser.addoption("--file", action="store", default="./env_config.json")
    parser.addoption("--host", action="store", default=None)
    parser.addoption("--action_mode", action="store", default=None)
    parser.addoption("--interactive_mode", action="store", default=None)
