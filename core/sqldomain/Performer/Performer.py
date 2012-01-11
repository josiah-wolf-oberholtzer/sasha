from sqlalchemy import Column, String

from sasha.core.sqldomain._DomainObject import _DomainObject


class Performer(_DomainObject):

    ### SQLALCHEMY ###

    name = Column(String)
