# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func, Text
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class Report(db.Model):

    __tablename__ = 'autotest_report'

    id = Column(BigInteger, primary_key=True)
    project_id = Column(BigInteger, nullable=False)
    module_id = Column(BigInteger, nullable=False)
    testcase_id = Column(BigInteger, nullable=False)
    result = Column(BOOLEAN, nullable=False)
    result_log = Column(Text, nullable=False)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, project_id, module_id, testcase_id, result, result_log, datachange_createtime=None,
                 datachange_lasttime=None, **kwargs):
        kwargs["project_id"] = project_id
        kwargs["module_id"] = module_id
        kwargs["testcase_id"] = testcase_id
        kwargs["result"] = result
        kwargs["result_log"] = result_log
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)
