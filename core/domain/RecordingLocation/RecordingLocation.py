from sqlalchemy import Column, String

from sasha.core.domain._Base import _Base
from sasha.core.domain.DomainObject import DomainObject


class RecordingLocation(_Base, DomainObject):

    ### SQLALCHEMY ###

    name = Column(String)
