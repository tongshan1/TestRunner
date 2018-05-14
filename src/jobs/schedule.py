# -*- coding: utf-8 -*-

from app import celery


@celery.task()
def add_together(a, b):
    return a + b


"""
单纯的异步执行
add_together.delay(1,2)

特定的时间执行
http://docs.celeryproject.org/en/master/userguide/calling.html#eta-and-countdown
from datetime import datetime, timedelta
after_one_minute = datetime.utcnow() + timedelta(minutes=1)
add_together.apply_async((2, 2), eta=after_one_minute)
"""
