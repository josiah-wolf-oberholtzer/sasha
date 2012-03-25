from sqlalchemy import Column, String

from sasha.core.domain._Base import _Base
from sasha.core.domain.DomainObject import DomainObject


class Performer(_Base, DomainObject):

    __fixture_paths__ = (
        'description',
        'name',
    )

    ### SQLALCHEMY ###

    description = Column(String)
    name = Column(String)
