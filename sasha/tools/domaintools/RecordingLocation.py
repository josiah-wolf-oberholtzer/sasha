from sqlalchemy import Column, String

from sasha.tools.domaintools.DomainObject import DomainObject


class RecordingLocation(DomainObject):

    ### SQLALCHEMY ###

    name = Column(String)
