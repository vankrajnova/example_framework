from selenium.webdriver.remote.webelement import WebElement as _webelement_

from time import sleep

from .config import *

from .waiting import waiting


class WebElement(_webelement_):

    def __init__(self, webelement: _webelement_):
        self.__dict__.update(webelement.__dict__)

    @waiting()
    def click(self, **kwargs):
        super().click()

    @waiting()
    def send_keys(self, *value, step=0, clear=True, **kwargs) -> None:
        value = "".join(value)
        if clear:
            self.clear()
            sleep(SLEEP_AFTER)
        if step == 0:
            super().send_keys(value)
        else:
            for sym in value:
                super().send_keys(sym)
                sleep(step)
        sleep(SLEEP_AFTER)
