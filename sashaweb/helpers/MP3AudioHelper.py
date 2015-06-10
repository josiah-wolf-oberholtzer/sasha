from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools
from sashaweb.helpers.Helper import Helper
from webhelpers.html import HTML, literal


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
        span_id = 'audioplayer_%s' % self.event.canonical_name
        #url = self.static_url
        span_tag = HTML.tag('span', id=span_id, c="temp")
        script_tag = HTML.tag(
            'script',
            type="text/javascript",
            c=literal('AudioPlayer.embed("%s", {soundFile: "%s", noinfo: "yes"});' %
                (span_id, self.static_url))
            )
        div_tag = HTML.tag('div', class_="mp3", c=[span_tag, script_tag])
        return div_tag

    @property
    def static_path(self):
        path = assettools.MP3Audio(self.event).path
        environment, path = path.partition(sasha_configuration.environment)[1:]
        return 'sashamedia:%s%s' % (environment, path)