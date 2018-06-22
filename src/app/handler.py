from functools import lru_cache, wraps
from flask import jsonify
from utils.utils import retcode, ERROR_MAP

import time


def register(bp, *params, **kwargs):
    """
    extend params
    :param bp:
    :param params:
    :param kwargs:
    :return:
    """

    def decorator(func):
        @bp.route(*params, **kwargs)
        @wraps(func)
        def method(*args, **kwargs):
            return func(*args, **kwargs)
        return method
    return decorator


def success(data=None):
    data = data if data is not None else {}
    assert isinstance(data, dict)
    data['ret'] = retcode.ret_1
    data['timestamp'] = int(time.time())

    return jsonify(data)


def get_error_message(ret):
    return ERROR_MAP[ret]


def fail(ret, error=None, data=None, args=None):
    data = data if data is not None else {}
    error = error if error is not None else get_error_message(ret)
    if args:
        args = isinstance(args, tuple) and args or (args,)
        error = error.format(*args)
    data['ret'] = ret
    data['error'] = error
    data['timestamp'] = int(time.time())

    return jsonify(data)