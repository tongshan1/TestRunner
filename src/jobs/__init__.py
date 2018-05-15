# -*- coding: utf-8 -*-

from app import celery

from . import schedule

"""
单纯的异步执行
func.delay(1,2)

特定的时间执行
http://docs.celeryproject.org/en/master/userguide/calling.html#eta-and-countdown
from datetime import datetime, timedelta
after_one_minute = datetime.utcnow() + timedelta(minutes=1)
func.apply_async((2, 2), eta=after_one_minute)
"""
