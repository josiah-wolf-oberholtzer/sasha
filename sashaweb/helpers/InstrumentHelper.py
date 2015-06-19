from sasha.tools import domaintools
from sashaweb.helpers.Helper import Helper
from webhelpers.html import HTML


class InstrumentHelper(Helper):

    def __init__(self, arg, request):
        Helper.__init__(self, request)
        if isinstance(arg, domaintools.Instrument):
            self.instrument = arg
        elif isinstance(arg, domaintools.Event):
            self.instrument = domaintools.Instrument.get_one(
                id=arg.instrument_id,
                )
        elif isinstance(arg, domaintools.Fingering):
            self.instrument = domaintools.Instrument.get_one(
                id=arg.instrument_id,
                )
        else:
            message = 'Expected Instrument, Fingering or Event instance, '
            message = message + 'got {!r} instead.'
            message = message.format(arg)
            raise ValueError(message)

    ### PUBLIC ATTRIBUTES ###

    @property
    def link(self):
        return HTML.tag('a', href=self.url, c=self.name)

    @property
    def name(self):
        return self.instrument.name

    @property
    def snakecase_name(self):
        return self.name.lower().replace(' ', '_')

    @property
    def url(self):
        return self.request.route_url(
            'instrument',
            instrument_name=self.instrument.name.lower().replace(' ', '-')
            )