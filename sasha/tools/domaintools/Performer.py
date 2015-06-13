from sqlalchemy import Column, String

from sasha.tools.domaintools.DomainObject import DomainObject


class Performer(DomainObject):

    ### CLASS VARIABLES ###

    __fixture_paths__ = (
        'description',
        'name',
        )

    ### SQLALCHEMY ###

    description = Column(String)
    name = Column(String)