from abjad.tools import stringtools
from webhelpers.html import HTML
import mongoengine


class Instrument(mongoengine.Document):

    ### MONGOENGINE ###

    description = mongoengine.StringField()
    key_names = mongoengine.ListField(mongoengine.StringField(max_length=5))
    name = mongoengine.StringField(required=True, max_length=50)
    parents = mongoengine.ListField(mongoengine.ReferenceField('Instrument'))
    transposition = mongoengine.IntField(default=0)

    ### PUBLIC METHODS ###

    def get_link_text(self):
        return self.name

    def get_link(self, request):
        href = self.get_url(request)
        text = self.get_link_text()
        return HTML.tag('a', href=href, c=text)

    def get_url(self, request):
        return request.route_url(
            'instrument',
            instrument_name=self.dash_case_name,
            )

    @classmethod
    def with_events(cls):
        from sasha.tools import newdomaintools
        return newdomaintools.Event.objects.only('instrument').distinct()

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return set(type(self).objects(parents=self))

    @property
    def dash_case_name(self):
        return stringtools.to_dash_case(self.name)

    @property
    def snake_case_name(self):
        return stringtools.to_snake_case(self.name)