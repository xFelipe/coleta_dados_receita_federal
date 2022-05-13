from functools import wraps
from time import sleep

from extract.helpers import log


def retry(times: int, exceptions=Exception, delay: int = 0):
    """
    Decorator que repete, até um determinado limite de vezes, a execução da
    função decorada caso ocorra um ou mais tipos de exceção ocorram.
    É possível definir um tempo de delay entre repetições (em segundos).
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(1, times):
                try:
                    return func(*args, **kwargs)
                except exceptions as error:
                    log.info(f'{error} - {i} time(s)')
                    sleep(delay)
            return func(*args, **kwargs)
        return wrapper
    return decorator
