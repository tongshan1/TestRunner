# -*- coding: utf-8 -*-
__author__ = 'sara'

from sqlalchemy import BigInteger
from sqlalchemy.dialects.postgresql.json import JSON
from . import Base


class Interface(Base):

    __tablename__ = ''
