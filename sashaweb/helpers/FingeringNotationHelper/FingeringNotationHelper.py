from sasha import sasha_configuration, Event, Fingering
from sasha.plugins import FingeringNotation
from sashaweb.helpers._Helper import _Helper
from sashaweb.helpers.FingeringHelper import FingeringHelper
from webhelpers.html import HTML


class FingeringNotationHelper(_Helper):

    def __init__(self, arg, request):
        _Helper.__init__(self, request)
        if isinstance(arg, Event):
            self.fingering = Fingering.get_one(id=arg.fingering_id)
        elif isinstance(arg, Fingering):
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
        path = FingeringNotation(self.fingering).path
        environment, path = path.partition(sasha_configuration.env)[1:]
        return 'sashamedia:%s%s' % (environment, path)
