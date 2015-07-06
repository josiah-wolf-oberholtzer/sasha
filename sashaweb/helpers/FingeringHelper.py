from abjad.tools import stringtools
from sasha.tools import domaintools
from webhelpers.html import HTML
from sashaweb.helpers.Helper import Helper


class FingeringHelper(Helper):

    ### INITIALIZER ###

    def __init__(self, arg, request):
        Helper.__init__(self, request)
        if isinstance(arg, domaintools.Event):
            self.event = arg
        elif isinstance(arg, domaintools.Fingering):
            self.event = domaintools.Event.get_one(fingering=arg)
        else:
            raise ValueError('Expected Fingering or Event instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def link(self):
        return HTML.tag('a', href=self.url, c=self.name)

    @property
    def name(self):
        fingering = domaintools.Fingering.get_one(id=self.event.fingering_id)
        return ' '.join([key.name for key in fingering.instrument_keys])

    @property
    def url(self):
        instrument = domaintools.Instrument.get_one(id=self.event.instrument_id)
        instrument_name = stringtools.to_dash_case(instrument.name)
        fingering = domaintools.Fingering.get_one(id=self.event.fingering_id)
        compact_representation = fingering.compact_representation
        return self.request.route_url(
            'fingering',
            instrument_name=instrument_name,
            compact_representation=compact_representation,
            )