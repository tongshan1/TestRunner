# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class Interface(db.Model):

    __tablename__ = 'Interface'

    InterfaceId = Column(Integer, primary_key=True)
    module_id = Column(Integer, nullable=False,)
    interface_name = Column(String(200), nullable=False, index=True)
    interface_url = Column(String(200), nullable=False,)
    interface_header = Column(String(200), nullable=False,)
    interface_body = Column(String(200), nullable=False,)
    interface_method = Column(String(10), nullable=False,)
    is_active = Column(BOOLEAN)
    create_time = Column(DateTime(True),)
    last_time = Column(DateTime(True),)

    def __init__(self, module_id, interface_name, interface_url, interface_header, interface_body, interface_method,
                 is_active=True, create_time=None, last_time=None, **kwargs):
        kwargs["module_id"] = 1
        kwargs["interface_name"] = interface_name
        kwargs["interface_url"] = interface_url
        kwargs["interface_header"] = str(interface_header)
        kwargs["interface_body"] = str(interface_body)
        kwargs["interface_method"] = interface_method
        kwargs["is_active"] = is_active
        kwargs["create_time"] = create_time
        kwargs["last_time"] = last_time

        super().__init__(**kwargs)
