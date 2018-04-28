# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, BOOLEAN, DateTime, func
from app import db


class Testcase_testgroup(db.Model):

    __tablename__ = 'autotest_testcase_testgroup'

    id = Column(BigInteger, primary_key=True)
    testcase_group_id = Column(BigInteger, index=True, nullable=False)
    testcase_id = Column(BigInteger, index=True, nullable=False)
    testcase_execution_order = Column(BigInteger, index=True, nullable=False,)
    is_active = Column(BOOLEAN, nullable=True, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, testcase_group_id, testcase_id, testcase_execution_order, is_active=True, datachange_createtime=None,
                 datachange_lasttime=None, **kwargs):
        kwargs["testcase_group_id"] = testcase_group_id
        kwargs["testcase_id"] = testcase_id
        kwargs["testcase_execution_order"] = testcase_execution_order
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)
