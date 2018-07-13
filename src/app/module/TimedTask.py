# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class TimedTask(db.Model):
    __tablename__ = 'autotest_timedtask'

    id = Column(BigInteger, primary_key=True)
    task_name = Column(String, nullable=False)
    task_type = Column(Integer, nullable=False, )
    testgroup_id = Column(BigInteger, index=True, nullable=False)
    task_desc = Column(String, nullable=False)
    task_config = Column(JSON)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())
