# -*- coding: utf-8 -*-
import json
from module.Module import Module

Method = {
    "GET": "GET",
    "POST": "POST",
    "PUT": "PUT",
    "DELETE": "DELETE",
    "PATCH": "PATCH",
    "HEAD": "HEAD",
    "OPTIONS": "OPTIONS"
}


def str_to_dict(tmp):
    try:
        if type(tmp) == str:
            return json.loads(tmp)
        elif tmp is None:
            return {}
        else:
            return tmp
    except ValueError:
        return {}
    except TypeError:
        return {}


def get_all_module():
    return Module.get_all()