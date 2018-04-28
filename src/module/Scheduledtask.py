# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class Scheduledtask(db.Model):

    __tablename__ = 'autotest_scheduledtask'

    id = Column(BigInteger, primary_key=True)
    task_name = Column(String(50), nullable=False)
    task_type = Column(Integer, nullable=False,)
    module_id = Column(BigInteger, index=True, nullable=False,)
    testcase_id = Column(BigInteger, index=True, nullable=False)
    task_desc = Column(String(200), nullable=False)
    time_interval = Column(Integer, nullable=False, default=24)
    last_execution_time = Column(DateTime(True), server_default=func.now())
    next_execution_time = Column(DateTime(True), server_default=func.now())
    task_result = Column(BOOLEAN, nullable=False, default=True)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, module_id, task_name, task_type,testcase_id, task_desc, last_execution_time,
                 next_execution_time, task_result, is_active=True, datachange_createtime=None, datachange_lasttime=None,
                 **kwargs):
        kwargs["task_name"] = task_name
        kwargs["task_type"] = task_type
        kwargs["module_id"] = module_id
        kwargs["testcase_id"] = testcase_id
        kwargs["task_desc"] = task_desc
        kwargs["last_execution_time"] = last_execution_time
        kwargs["next_execution_time"] = next_execution_time
        kwargs["task_result"] = task_result
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)
