from sasha.tools import domaintools
from sashaweb.helpers._Helper import _Helper
from webhelpers.html import HTML


class InstrumentHelper(_Helper):

    def __init__(self, arg, request):
        _Helper.__init__(self, request)
        if isinstance(arg, domaintools.Instrument):
            self.instrument = arg
        elif isinstance(arg, domaintools.Event):
            self.instrument = domaintools.Instrument.get_one(id=arg.instrument_id)
        elif isinstance(arg, domaintools.Fingering):
            self.instrument = domaintools.Instrument.get_one(id=arg.instrument_id)
        else:
            raise ValueError('Expected Instrument, Fingering or Event instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def link(self):
        return HTML.tag('a', href=self.url, c=self.name)

    @property
    def name(self):
        return self.instrument.name

    @property
    def url(self):
        return self.request.route_url('single_instrument',
            instrument_name=self.instrument.name.lower().replace(' ', '-'))