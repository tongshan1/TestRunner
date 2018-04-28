# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class TestInterfacecase(db.Model):

    __tablename__ = 'autotest_interface_testcase'

    id = Column(BigInteger, primary_key=True)
    interface_url = Column(String(255), nullable=False)
    testcase_name = Column(String(200), nullable=False)
    testcase_header = Column(JSON, nullable=False)
    testcase_body = Column(JSON, nullable=False)
    testcase_response = Column(JSON, nullable=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, interface_url, testcase_name, testcase_header, testcase_body, testcase_response,
                 is_active=True, datachange_createtime=None, datachange_lasttime=None, **kwargs):
        kwargs["interface_url"] = interface_url
        kwargs["testcase_name"] = testcase_name
        kwargs["testcase_header"] = testcase_header
        kwargs["testcase_body"] = testcase_body
        kwargs["testcase_response"] = testcase_response
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)


class TestUIcase(db.Model):

    __tablename__ = 'autotest_UI_testcase'

    id = Column(BigInteger, primary_key=True)
    testcase_name = Column(String(200), nullable=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, interface_id, testcase_name, testcase_header, testcase_body, testcase_response,
                 is_active=True, datachange_createtime=None, datachange_lasttime=None, **kwargs):
        kwargs["testcase_name"] = testcase_name
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)

