from sqlalchemy import Column, String

from sasha.core.domain.DomainObject import DomainObject


class RecordingLocation(DomainObject):

    ### SQLALCHEMY ###

    name = Column(String)
