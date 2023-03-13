from time import sleep, time
from .config import *


def waiting():
    def decorator(func):
        def wrapper(*args, **kwargs):
            start = time()
            timeout = kwargs["TIMEOUT"] if kwargs.get("TIMEOUT") else TIMEOUT
            steptime = kwargs["STEPTIME"] if kwargs.get("STEPTIME") else STEPTIME
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
