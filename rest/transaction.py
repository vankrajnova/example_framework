import functools
import time
from json import JSONDecodeError
from typing import Callable
from urllib.parse import urljoin
import requests
from backoff import on_exception, expo

from model.user import User
from rest.exceptions import error_by_status_code

from useful_methods.representation import pretty_json, shorten_str


TIMEOUT = 60
STEP_TIME = 0.2


class RestTransaction:

    def __init__(self, app, transaction_name: str):
        self._app = app
        self.name = transaction_name
        self.response = None
        self.event_log = [f"\nТранзакция: {self.name}"]
        self.rest_session = requests.session()

    def clean_log(self):
        self.__init__(self._app, self.name)

    def add_event(self, event_message: str):
        self.event_log.append(event_message)

    @staticmethod
    def logger(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            self.event_log.append(f"method = {args[0]}")
            self.event_log.append(f"path = {args[1]}")
            if "data" in kwargs:
                self.event_log.append(pretty_json(kwargs["data"]))
            if "headers" in kwargs:
                self.event_log.append(str(kwargs["headers"]))
            if "json" in kwargs:
                self.event_log.append(f'request json: \n{pretty_json(kwargs["json"])}')
            result = func(self, *args, **kwargs)
            self.event_log.append(f"response: \n{shorten_str(pretty_json(result))}")
            return result

        return wrapper

    @on_exception(expo, requests.exceptions.HTTPError, max_tries=5)
    def auth(self, logged_in_user: User = None) -> dict:
        login = logged_in_user.info.account_name if logged_in_user else "administrator"
        password = logged_in_user.info.password if logged_in_user else "5ecr3t"
        url_for_auth = urljoin(
            self._app.config.host, f"inrights/api/auth/login?login={login}&password={password}"
        )
        response = self.rest_session.post(url_for_auth)
        response.raise_for_status()
        return response.json()

    def logout(self):
        url_for_logout = urljoin(self._app.config.host, "inrights/api/auth/logout")
        self.rest_session.post(url_for_logout)

    @logger
    def call_request(
            self, request_type: str, path: str, logged_in_user: User = None, **kwargs
    ) -> dict | str:
        try:
            self.auth(logged_in_user=logged_in_user)
            self.response = self.rest_session.request(
                request_type, urljoin(self._app.config.host, path), **kwargs
            )
            self.handle_status()
            return self.response.json()
        except JSONDecodeError:
            return self.response.text
        finally:
            self.logout()

    def handle_status(self):
        if 400 <= self.response.status_code < 600:
            self.event_log.append(
                f"response: \n{shorten_str(pretty_json(self.response.json()))}"
            )
            self.raise_exception(
                exception=error_by_status_code(self.response.status_code)
            )

    def raise_exception(
            self, exception_message: str = None, exception: Exception = None
    ):
        self.print_log()
        if exception:
            raise exception
        elif exception_message:
            raise Exception(exception_message)

    def check_items(self) -> list[dict]:
        try:
            return self.response.json()["items"]
        except KeyError:
            self.raise_exception('В ответе нет ключа "items"')

    def print_log(self):
        print("\n".join(self.event_log))

    def get_log(self) -> str:
        return "\n".join(self.event_log)


def wait(timeout: int = TIMEOUT, step_time: int | float = STEP_TIME) -> Callable:
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            last_error = None

            while (time.time() - start) < timeout:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    time.sleep(step_time)
            raise last_error

        return wrapper

    return decorator
