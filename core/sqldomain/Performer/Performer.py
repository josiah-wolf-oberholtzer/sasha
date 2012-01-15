from sqlalchemy import Column, String

from sasha.core.sqldomain._Base import _Base
from sasha.core.sqldomain._DomainObject import _DomainObject


class Performer(_Base, _DomainObject):

    __fixture_paths__ = (
        'description',
        'name',
    )

    ### SQLALCHEMY ###

    description = Column(String)
    name = Column(String)
