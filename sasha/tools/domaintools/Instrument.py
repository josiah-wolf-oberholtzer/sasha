from abjad.tools import stringtools
from sasha.tools.domaintools.DomainObject import DomainObject
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import backref, relationship
from webhelpers.html import HTML


class Instrument(DomainObject):

    ### CLASS VARIABLES ###

    __fixture_paths__ = (
        'description',
        'instrument_keys.name',
        'name',
        'parent.name',
        'transposition',
        )

    ### SQLALCHEMY ###

    description = Column(String, nullable=True)
    name = Column(String, unique=True)
    parent_id = Column(Integer, ForeignKey('instruments.id'), nullable=True)
    transposition = Column(Integer)

    @declared_attr
    def children(cls):
        return relationship(
            'Instrument',
            backref=backref('parent', remote_side=lambda: cls.id),
            )

    ### PUBLIC METHODS ###

    def get_link(self, request):
        href = self.get_url(request)
        text = self.name
        return HTML.tag('a', href=href, c=text)

    def get_url(self, request):
        return request.route_url(
            'instrument',
            instrument_name=self.dash_case_name,
            )

    @classmethod
    def with_events(cls):
        from sasha import sasha_configuration
        from sasha.tools.domaintools.Event import Event
        query = sasha_configuration.get_session().query(cls)
        query = query.join(Event).distinct().all()
        return query

    ### PUBLIC PROPERTIES ###

    @property
    def dash_case_name(self):
        return stringtools.to_dash_case(self.name)

    @property
    def snake_case_name(self):
        return stringtools.to_snake_case(self.name)