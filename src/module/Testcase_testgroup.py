# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, BOOLEAN, DateTime, func
from app import db

from .Testcasegroup import Testcasegroup
from .Testcase import TestInterfacecase, TestUIcase


class Testcase_testgroup(db.Model):
    __tablename__ = 'autotest_testcase_testgroup'

    id = Column(BigInteger, primary_key=True)
    testcase_group_id = Column(BigInteger, index=True, nullable=False)
    testcase_id = Column(BigInteger, index=True, nullable=False)
    testcase_execution_order = Column(BigInteger, index=True, nullable=False, )
    is_active = Column(BOOLEAN, nullable=True, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __repr__(self):
        return self.module_name

    @property
    def testcase_group(self):
        return Testcasegroup.query.get(self.testcase_group_id)

    @testcase_group.setter
    def testcase_group(self, testcase_group):
        self.testcase_group_id = testcase_group.id

    @property
    def testcase(self):
        if self.testcase_group.id == 1:
            return TestInterfacecase.query.get(self.testcase_id)

    @testcase.setter
    def testcase(self, testcase):
        self.testcase_id = testcase.id

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_by_group_id(cls, group_id):
        return cls.query.filter(testcase_group_id=group_id).all()

