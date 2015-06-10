from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools
from sashaweb.helpers._Helper import _Helper
from sashaweb.helpers.FingeringHelper import FingeringHelper
from webhelpers.html import HTML


class FingeringNotationHelper(_Helper):

    def __init__(self, arg, request):
        _Helper.__init__(self, request)
        if isinstance(arg, domaintools.Event):
            self.fingering = domaintools.Fingering.get_one(id=arg.fingering_id)
        elif isinstance(arg, domaintools.Fingering):
            self.fingering = arg
        else:
            raise ValueError('Expected Event or Fingering instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def image(self):
        return HTML.tag('img', src=self.static_url)

    @property
    def image_link(self):
        fingering_url = FingeringHelper(self.fingering, self.request).url
        return HTML.tag('a', href=fingering_url, c=self.image)

    @property
    def static_path(self):
        path = assettools.FingeringNotation(self.fingering).path
        environment, path = path.partition(sasha_configuration.environment)[1:]
        return 'sashamedia:%s%s' % (environment, path)