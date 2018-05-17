# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, String, BOOLEAN, DateTime, func
from app import db
from .Module import Module


class TestCaseType(db.Model):
    __tablename__ = 'autotest_testcase_type'

    id = Column(BigInteger, primary_key=True)
    type_code = Column(BigInteger, index=True, nullable=False)
    type_name = Column(String(500), nullable=False)
    is_active = Column(BOOLEAN, nullable=False)

    def __repr__(self):
        return self.type_name


class Testcasegroup(db.Model):
    __tablename__ = 'autotest_testcasegroup'

    id = Column(BigInteger, primary_key=True)
    module_id = Column(BigInteger, index=True, nullable=False)
    testcase_group_name = Column(String(200), nullable=False)
    testcase_type = Column(BigInteger, index=True, nullable=False,)
    testcase_desc=Column(String(500), nullable=False)
    is_active = Column(BOOLEAN, nullable=False)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __repr__(self):
        return self.module_name

    @property
    def module(self):
        return Module.query.get(self.module_id)

    @module.setter
    def module(self, module):
        self.module_id = module.id

    @property
    def type(self):
        return TestCaseType.query.get(self.testcase_type)

    @type.setter
    def type(self, type):
        self.testcase_type = type.id

# class Module(db.Model):
#     __tablename__ = 'autotest_module'
#     id = Column(BigInteger, primary_key=True)
#     project_id = Column(BigInteger, index=True, nullable=False)
#     module_name = Column(String(50), nullable=False)
#     module_testers = Column(String(50), nullable=False)
#     module_developer = Column(String(50), nullable=False)
#     module_version = Column(String(100), nullable=False)
#     module_desc = Column(String(500), nullable=False)
#     is_active = Column(BOOLEAN, nullable=False, default=True)
#     datachange_createtime = Column(DateTime(True), server_default=func.now())
#     datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())
#
#     def __repr__(self):
#         return self.module_name
#
#     @property
#     def project(self):
#         return Project.query.get(self.project_id)
#
#     @project.setter
#     def project(self, project):
#         self.project_id = project.id
