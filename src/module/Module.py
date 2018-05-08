# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


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

    def __init__(self, project_id, module_name, module_testers, module_developer, module_version, module_desc,
                 is_active=True, datachange_createtime=None, datachange_lasttime=None, **kwargs):
        kwargs["project_id"] = project_id
        kwargs["module_name"] = module_name
        kwargs["module_testers"] = module_testers
        kwargs["module_developer"] = module_developer
        kwargs["module_version"] = module_version
        kwargs["module_desc"] = module_desc
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)
