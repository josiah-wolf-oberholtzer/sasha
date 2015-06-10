from sasha import sasha_configuration, Event
from sasha.tools.assettools import PartialTrackingPlot
from sashaweb.helpers._Helper import _Helper
from sashaweb.helpers.EventHelper import EventHelper
from webhelpers.html import HTML


class PartialTrackingPlotHelper(_Helper):

    def __init__(self, arg, request):
        _Helper.__init__(self, request)
        if isinstance(arg, Event):
            self.event = arg
        else:
            raise ValueError('Expected Event instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def image(self):
        return HTML.tag('img', src=self.static_url)

    @property
    def image_link(self):
        event_url = EventHelper(self.event, self.request).url
        return HTML.tag('a', href=event_url, c=self.image)

    @property
    def static_path(self):
        path = PartialTrackingPlot(self.event).path
        environment, path = path.partition(sasha_configuration.env)[1:]
        return 'sashamedia:%s%s' % (environment, path)
