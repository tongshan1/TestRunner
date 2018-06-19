# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, Boolean
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class SystemSetting(db.Model):

    """
    type:1 runner_setting
    """
    __tablename__ = 'autotest_system_setting'

    id = Column(Integer, primary_key=True)
    key = Column(String(32), nullable=False, unique=True)
    type = Column(Integer, nullable=False)
    value = Column(JSON)
    desc = Column(Text)
    is_active = Column(Boolean, default=True)

    @classmethod
    def get_runner_setting(cls):
        try:
            return cls.query.filter_by(type=1).all()
        except NoResultFound:
            return []

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)