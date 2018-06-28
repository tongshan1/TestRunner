# -*- coding: utf-8 -*-
import uuid
import time


def device_hash():
    return uuid.uuid4().hex


def ts():
    return str(int(time.time()))

