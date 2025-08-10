from functools import wraps
from loguru import logger
from random import gauss


# def move_log(func):
#     """decorator for logging Player move"""
#     @wraps(func)
#     def inner(o):
#         if o.is_alive():
#             s = f"{o.id}`s {o.type} move"
#             logger.info(s)
#         func(o)
#
#     return inner

def move_log(is_log: bool):
    """decorator for logging Player move"""
    def log_decorator(func):
        @wraps(func)
        def inner(o):
            if o.is_alive():
                s = f"{o.id}`s {o.type} move" if is_log else "meow"
                logger.info(s)
            func(o)

        return inner
    return log_decorator

def need_ill() -> bool:
    return gauss(mu=0.5, sigma=0.1) * gauss(mu=0.5, sigma=0.1) > 0.3

def get_player_startup_hp():
    return int(gauss(mu=100, sigma=25))

def get_apple_startup_hp():
    return int(gauss(mu=100, sigma=25))