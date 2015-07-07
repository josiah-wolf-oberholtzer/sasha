from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools
from sashaweb.helpers.Helper import Helper
from webhelpers.html import HTML


class MP3AudioHelper(Helper):

    def __init__(self, arg, request):
        Helper.__init__(self, request)
        if isinstance(arg, domaintools.Event):
            self.event = arg
        else:
            raise ValueError('Expected Event instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def audio(self):
        source_tag = HTML.tag('source', type_='audio/mp3', src=self.static_url)
        audio_tag = HTML.tag('audio', controls='controls', c=[source_tag])
        div_tag = HTML.tag('div', class_='mp3', c=[audio_tag])
        return div_tag

    @property
    def static_path(self):
        path = assettools.MP3Audio(self.event).path
        environment, path = path.partition(sasha_configuration.environment)[1:]
        return 'sashamedia:%s%s' % (environment, path)