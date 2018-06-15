# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm.exc import NoResultFound
from app import db


class SystemSetting(db.Model):
    __tablename__ = 'autotest_system_setting'

    id = Column(Integer, primary_key=True)
    key = Column(String(32), nullable=False, unique=True)
    value = Column(Text)
    is_active = Column(Boolean)

    @classmethod
    def get_runner_setting(cls):
        try:
            return cls.query.filter_by(key="runner_setting").one()
        except NoResultFound:
            return []