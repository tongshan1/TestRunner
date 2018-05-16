# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class Interface(db.Model):

    __tablename__ = 'autotest_Interface'

    id = Column(BigInteger, primary_key=True)
    module_id = Column(BigInteger)
    interface_name = Column(String(200), nullable=False, index=True)
    interface_url = Column(String(255), nullable=False)
    interface_header = Column(JSON, nullable=True)
    interface_body = Column(JSON, nullable=True)
    interface_method = Column(String(10), nullable=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, interface_name, interface_url, interface_header, interface_body, interface_method,
                 is_active=True, datachange_createtime=None, datachange_lasttime=None, **kwargs):
        kwargs["interface_name"] = interface_name
        kwargs["interface_url"] = interface_url
        kwargs["interface_header"] = interface_header
        kwargs["interface_body"] = interface_body
        kwargs["interface_method"] = interface_method
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)
