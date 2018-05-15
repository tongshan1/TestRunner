# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, String, BOOLEAN, DateTime, func
from app import db


class User(db.Model):
    __tablename__ = 'autotest_user'

    id = Column(BigInteger, primary_key=True)
    login_name = Column(String(20), nullable=False)
    user_name = Column(String(20), nullable=False)
    email = Column(String(100), nullable=False)
    phone = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    is_active = Column(BOOLEAN, nullable=False)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    def __init__(self, login_name, user_name, email, phone, description,
                 is_active=True, datachange_createtime=None, datachange_lasttime=None, **kwargs):
        kwargs["login_name"] = login_name
        kwargs["user_name"] = user_name
        kwargs["email"] = email
        kwargs["phone"] = phone
        kwargs["description"] = description
        kwargs["is_active"] = is_active
        kwargs["datachange_createtime"] = datachange_createtime
        kwargs["datachange_lasttime"] = datachange_lasttime

        super().__init__(**kwargs)
