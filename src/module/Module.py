# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, String, BOOLEAN, DateTime, func
from app import db
from .Project import Project


class Module(db.Model):
    __tablename__ = 'autotest_module'

    id = Column(BigInteger, primary_key=True)
    project_id = Column(BigInteger, index=True, nullable=False)
    module_name = Column(String(50), nullable=False)
    module_testers = Column(String(50), nullable=False)
    module_developer = Column(String(50), nullable=False)
    module_version = Column(String(100), nullable=False)
    module_desc = Column(String(500), nullable=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __repr__(self):
        return self.module_name

    @property
    def project(self):
        return Project.query.get(self.project_id)

    @project.setter
    def project(self, project):
        self.project_id = project.id

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_name(cls, module_name):
        return cls.query.flter_by(module_name=module_name)