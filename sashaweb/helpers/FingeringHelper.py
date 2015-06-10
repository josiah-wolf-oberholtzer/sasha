from sasha.tools import domaintools
from webhelpers.html import HTML
from sashaweb.helpers.Helper import Helper


class FingeringHelper(Helper):

    def __init__(self, arg, request):
        Helper.__init__(self, request)
        if isinstance(arg, domaintools.Fingering):
            self.fingering = arg
        elif isinstance(arg, domaintools.Event):
            self.fingering = domaintools.Fingering.get_one(id=arg.fingering_id)
        else:
            raise ValueError('Expected Fingering or Event instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def link(self):
        return HTML.tag('a', href=self.url, c=self.name)

    @property
    def name(self):
        fingering = domaintools.Fingering.get_one(id=self.fingering.id)
        return ' '.join([key.name for key in fingering.instrument_keys])

    @property
    def url(self):
        instrument_name = domaintools.Instrument.get_one(id=self.fingering.instrument_id).name
        return self.request.route_url('single_fingering',
            instrument_name=instrument_name.lower().replace(' ', '-'),
            compact_representation=self.fingering.compact_representation)