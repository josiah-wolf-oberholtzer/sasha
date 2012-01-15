from sqlalchemy import Column, String

from sasha.core.domain._Base import _Base
from sasha.core.domain._DomainObject import _DomainObject


class Performer(_Base, _DomainObject):

    __fixture_paths__ = (
        'description',
        'name',
    )

    ### SQLALCHEMY ###

    description = Column(String)
    name = Column(String)
