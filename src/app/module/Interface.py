# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, String, BOOLEAN, DateTime, Text, func
from sqlalchemy.dialects.postgresql.json import JSON
from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.logger import logger
from .Module import Module


class Interface(db.Model):
    __tablename__ = 'autotest_Interface'

    id = Column(BigInteger, primary_key=True)
    module_id = Column(BigInteger)
    interface_name = Column(String, nullable=False, index=True)
    interface_url = Column(Text, nullable=False)
    interface_header = Column(JSON, nullable=True)
    interface_query = Column(JSON, nullable=True)
    interface_body = Column(JSON, nullable=True)
    interface_method = Column(String, nullable=False)
    interface_desc = Column(Text, nullable=True)
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
    def get_all_oder_by_module(cls):
        return cls.query.filter_by(is_active=True).order_by(
            cls.module_id)

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_url_method(cls, url, method):
        interface = None
        try:
            interface = cls.query.filter_by(interface_url=url, interface_method=method).one()
        except NoResultFound:
            logger.error("没有找到！")
        return interface
