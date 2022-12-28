from json import JSONDecodeError
from time import time, sleep

import requests

from rest.exceptions import error_by_status_code
from useful_methods.representation import json_as_pretty_str


TIMEOUT = 60
STEPTIME = 0.2


class RestTransaction:
    def __init__(self, app, transaction_name):
        self._config = app.config
        self.name = transaction_name
        self._request_url = None
        self._request_json = None
        self._request_headers = None
        self.response = None
        self.events = [f'## Транзакция (REST): {self.name}\n']

    def clean_log(self):
        self._request_url = None
        self._request_json = None
        self.response = None
        self.events = []
        self.events.append(f'## Транзакция (REST): {self.name}\n')

    def add_event(self, event_message):
        self.events.append(f'# {event_message}\n')

    def add_info(self, info_message):
        self.events.append(info_message.lstrip())

    def set_request_url(self, request_url):
        self._request_url = request_url
        self.add_info(f'request_url = {self._request_url}')

    def set_request_json(self, request_json):
        self._request_json = request_json
        self.add_info(f'request_json: \n{json_as_pretty_str(self._request_json)}')

    def set_request_headers(self, request_headers):
        self._request_headers = request_headers
        self.add_info(f'request_headers: \n{json_as_pretty_str(self._request_headers)}')

    def _send_request(self, request_type="GET", url=None, json=None, headers=None,
                      login="administrator", password="5ecr3t"):
        url_for_auth = fr'{self._config.host}/inrights/api/auth/login?login={login}&password={password}'
        rest_session = requests.session()
        request_by_type = {"GET": rest_session.get, "POST": rest_session.post, "PUT": rest_session.put,
                           "DELETE": rest_session.delete}
        try:
            start = time()
            while time() - start < 2:
                response = rest_session.post(url_for_auth)
                if response.status_code == 200:
                    break
                else:
                    sleep(.05)
            response = request_by_type[request_type](url, json=json, headers=headers)
            start = time()
            while (time() - start) < 5:
                if response.content is not None:
                    return response
                else:
                    sleep(.05)
        finally:
            rest_session.post(url=fr'{self._config.host}/inrights/api/auth/logout')

    def call_request(self, request_type, logged_in_user=None):
        if logged_in_user is None:
            self.response = self._send_request(request_type=request_type, url=self._request_url,
                                               json=self._request_json, headers=self._request_headers)
        else:
            self.response = self._send_request(request_type=request_type, url=self._request_url,
                                               json=self._request_json, headers=self._request_headers,
                                               login=logged_in_user.account_name, password=logged_in_user.password)
        """Добавлено ожидание тела запроса"""
        timeout = 5
        start_time = time()
        while (time() - start_time) < timeout:
            if self.response.text is None:
                sleep(.05)
            else:
                break
        try:
            self.add_info(f'response: \n{json_as_pretty_str(self.response.json())}')
        except JSONDecodeError:
            self.add_info(f'response: "{self.response.text}"')

        # new handler of status codes. Raise only 4XX and 5XX.
        self.raise_exception(exception=error_by_status_code(self.response.status_code))

        try:
            if self.response.text not in ['', 'File delete']:
                if len(self.response.text) != 36:
                    self.response.json()
        except JSONDecodeError:
            raise Exception(f'Не удалось распарсить json.\n{self.get_log()}')
        return self.response

    def raise_exception(self, exception_message=None, exception=None):
        if exception:
            self.print_log()
            raise exception
        elif exception_message:
            self.print_log()
            raise Exception(exception_message)

    def print_log(self):
        print()
        print('\n'.join(self.events))

    def get_log(self):
        return '\n' + '\n'.join(self.events)


def waiting():
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time()
            timeout = kwargs.get("TIMEOUT") if kwargs.get("TIMEOUT") is not None else TIMEOUT
            steptime = kwargs.get("STEPTIME") if kwargs.get("STEPTIME") is not None else STEPTIME

            last_error = None

            while time() - start < timeout:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    sleep(steptime)
            raise last_error
        return wrapper
    return decorator
