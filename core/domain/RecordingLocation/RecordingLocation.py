from sqlalchemy import Column, String

from sasha.core.domain._Base import _Base
from sasha.core.domain._DomainObject import _DomainObject


class RecordingLocation(_Base, _DomainObject):

    ### SQLALCHEMY ###

    name = Column(String)
