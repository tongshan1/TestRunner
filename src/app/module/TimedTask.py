# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func, Text
from sqlalchemy.dialects.postgresql.json import JSON
from app import db


class TimedTask(db.Model):
    __tablename__ = 'autotest_timedtask'

    id = Column(BigInteger, primary_key=True)
    task_name = Column(String, nullable=False)
    task_type = Column(Integer, nullable=False, )
    testgroup_id = Column(BigInteger, index=True, nullable=False)
    task_cron = Column(Text)
    task_desc = Column(String, nullable=False)
    is_active = Column(BOOLEAN, nullable=False, default=True)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_all_active(cls):
        return cls.query.fiter(is_active=True).all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get(id)


class Job(db.Model):
    """
    运行的job
    """

    __tablename = "autotest_job"

    id = Column(BigInteger, primary_key=True)
    task_id = Column(Integer, nullable=False)
    build_no = Column(Integer, index=True, nullable=False)
    status = Column(String, nullable=False)
    result = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)
    datachange_createtime = Column(DateTime(True), server_default=func.now())
    datachange_lasttime = Column(DateTime(True), index=True, onupdate=func.now())

    @classmethod
    def get_last_job(cls, task_id):
        return cls.query.fiter_by(task_id=task_id).order_by(cls.build_no.desc()).first()

