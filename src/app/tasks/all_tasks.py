# -*- coding: utf-8 -*-
from app import celery
from importlib import import_module, reload


def import_string(import_name):
    import_name = str(import_name).replace(':', '.')
    modules = import_name.split('.')
    mod = import_module(modules[0])
    for comp in modules[1:]:
        if not hasattr(mod, comp):
            reload(mod)
        mod = getattr(mod, comp)
    return mod


@celery.task
def execute(func, *args, **kwargs):
    func = import_string(func)
    return func(*args, **kwargs)
