from functools import lru_cache, wraps


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
            pass