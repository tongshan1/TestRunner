# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, String, BOOLEAN, DateTime, func
from sqlalchemy.dialects.mysql.json import JSON
from app import db
from .Module import Module


class TestInterfacecase(db.Model):
    __tablename__ = 'autotest_interface_testcase'

    id = Column(BigInteger, primary_key=True)
    interface_url = Column(String, nullable=False)
    testcase_name = Column(String, nullable=False)
    module_id= Column(BigInteger, nullable=False)
    testcase_method = Column(String, nullable=False)
    testcase_header = Column(JSON)
    testcase_query = Column(JSON)
    testcase_body = Column(JSON)
    testcase_verification = Column(JSON)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    @property
    def module(self):
        return Module.query.get(self.module_id)

    @module.setter
    def module(self, module):
        self.module_id = module.id

    @classmethod
    def get_all(cls):
        return cls.query.filter_by(is_active=True).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)


class TestUIcase(db.Model):
    __tablename__ = 'autotest_UI_testcase'

    id = Column(BigInteger, primary_key=True)
    testcase_name = Column(String, nullable=False)
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

    @property
    def module(self):
        return Module.query.get(self.module_id)

    @module.setter
    def module(self, module):
        self.module_id = module.id

