# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger, Column, Integer, String, BOOLEAN, DateTime, func
from app import db


class CancelVcOrderLog(db.Model):
    __tablename__ = 'cancel_vc_order_logs'

    id = Column(BigInteger, primary_key=True)
    order_id = Column(BigInteger, nullable=False, index=True)
    message = Column(String(255))
    success = Column(BOOLEAN, default=False)
