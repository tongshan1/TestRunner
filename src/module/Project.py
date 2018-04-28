# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class Project(db.Model):

    __tablename__ = 'autotest_project'

    id = Column(BigInteger, primary_key=True)
    project_name = Column(String(50), nullable=False)
    project_testers = Column(String(50), nullable=False)
    project_developer = Column(String(50), nullable=False)
    project_version = Column(String(100), nullable=False)
    project_desc = Column(String(500), nullable=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, project_name, project_testers, project_developer, project_version, project_desc,
                 is_active=True, datachange_createtime=None, datachange_lasttime=None, **kwargs):
        kwargs["project_name"] = project_name
        kwargs["project_testers"] = project_testers
        kwargs["project_developer"] = project_developer
        kwargs["project_version"] = project_version
        kwargs["project_desc"] = project_desc
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)
