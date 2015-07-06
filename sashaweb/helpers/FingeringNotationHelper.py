from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools
from sashaweb.helpers.Helper import Helper
from sashaweb.helpers.FingeringHelper import FingeringHelper
from webhelpers.html import HTML


class FingeringNotationHelper(Helper):

    def __init__(self, arg, request):
        Helper.__init__(self, request)
        if isinstance(arg, domaintools.Event):
            self.event = arg
        elif isinstance(arg, domaintools.Fingering):
            self.event = domaintools.Event.get_one(fingering=arg)
        else:
            raise ValueError('Expected Event or Fingering instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def image(self):
        return HTML.tag('img', src=self.static_url)

    @property
    def image_link(self):
        fingering_url = FingeringHelper(self.event, self.request).url
        return HTML.tag('a', href=fingering_url, c=self.image)

    @property
    def static_path(self):
        path = assettools.FingeringNotation(self.event).path
        environment, path = path.partition(sasha_configuration.environment)[1:]
        return 'sashamedia:%s%s' % (environment, path)