# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func, Text
from sqlalchemy.dialects.postgresql.json import JSON
from .Testcase_testgroup import Testcase_testgroup
from .Testcasegroup import Testcasegroup
from app import db


class Result(db.Model):
    __tablename__ = 'autotest_result'
    id = Column(BigInteger, primary_key=True)
    report_id = Column(BigInteger, nullable=False)
    testcase_testgroup_id = Column(BigInteger, nullable=False)
    result = Column(Integer, nullable=False)
    note = Column(Text, nullable=True)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    @property
    def testcase_testgroup(self):
        return Testcase_testgroup.query.get(self.testcase_testgroup_id)

    @testcase_testgroup.setter
    def testcase_testgroup(self, testcase_testgroup):
        self.testcase_testgroup_id = testcase_testgroup.id

    @property
    def report(self):
        return Report.query.get(self.report_id)

    @report.setter
    def report(self, report):
        self.report_id = report.id

    def __init__(self, report_id, testcase_testgroup_id, result, note, **kwargs):
        self.report_id = report_id
        self.testcase_testgroup_id = testcase_testgroup_id
        self.result = result
        self.note = note

        super().__init__(**kwargs)

    @classmethod
    def get_by_report_id(cls, report_id):
        return cls.query.filter_by(report_id=report_id).all()


class Report(db.Model):

    __tablename__ = 'autotest_report'

    id = Column(BigInteger, primary_key=True)
    testgroup_id = Column(BigInteger, nullable=False)
    result = Column(BOOLEAN, nullable=True)
    fail = Column(JSON, nullable=True)
    error = Column(JSON, nullable=True)
    success = Column(JSON, nullable=True)
    total = Column(BigInteger, nullable=True)
    result_log = Column(Text, nullable=True)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, testgroup_id,  **kwargs):
        kwargs["testgroup_id"] = testgroup_id

        super().__init__(**kwargs)

    @property
    def testgroup(self):
        return Testcasegroup.query.get(self.testgroup_id)

    @testgroup.setter
    def testgroup(self, testgroup):
        self.testgroup_id = testgroup.id

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)
