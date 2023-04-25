import sys
import logging
#import client_log_config, server_log_config
import inspect

if sys.argv[0] == 'client.py':
    logger = logging.getLogger('client')
else:
    logger = logging.getLogger('server')


def log(func):
    def output_func(*args, **kavargs):
        r = func(*args, **kavargs)
        logger.debug(f'Функция {func.__name__} вызванна с аргументами {args, kavargs}'
                    f'из функции {inspect.stack()[1][3]}')
        return r
    return output_func

