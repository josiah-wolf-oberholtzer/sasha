from sqlalchemy import Column, Integer
from sqlalchemy.ext.declarative import declarative_base


class _Base(object):

    ### SQLALCHEMY ###

    id = Column(Integer, primary_key=True)

_Base = declarative_base(cls=_Base)
