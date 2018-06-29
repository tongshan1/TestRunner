# -*- coding: utf-8 -*-
import json
from module.Testcasegroup import TestCaseType
from module.Module import Module
from module.System_setting import SystemSetting

Method = [
    ("GET", "GET"),
    ("POST", "POST"),
    ("PUT", "PUT"),
    ("DELETE", "DELETE"),
    ("PATCH", "PATCH"),
    ("HEAD", "HEAD"),
    ("OPTIONS", "OPTIONS")
]

Type = [
    ("None", "None"),
    ("int", "Integer"),
    ("str", "String"),
    ("float", "Float"),
    ("list", "List"),
    ("dict", "Dict"),

]


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


def get_types():
    return TestCaseType.get_all()


def get_runner_setting():
    return SystemSetting.get_runner_setting()