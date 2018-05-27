# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text
from app import db


class SystemSetting(db.Model()):
    __tablename__ = 'autotest_system_setting'

    id = Column(Integer, primary_key=True)
    key = Column(String(32), nullable=False, unique=True)
    value = Column(Text, nullable=False)
