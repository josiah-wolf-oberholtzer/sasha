from sqlalchemy import Column, String

from sasha.core.domain.DomainObject import DomainObject


class Performer(DomainObject):

    __fixture_paths__ = (
        'description',
        'name',
    )

    ### SQLALCHEMY ###

    description = Column(String)
    name = Column(String)
