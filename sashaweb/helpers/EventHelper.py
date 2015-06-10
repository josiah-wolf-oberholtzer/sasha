from sasha.tools import domaintools
from sashaweb.helpers.Helper import Helper
from webhelpers.html import HTML


class EventHelper(Helper):

    def __init__(self, arg, request):
        Helper.__init__(self, request)
        if isinstance(arg, domaintools.Event):
            self.event = arg
        else:
            raise ValueError('Expected Event instance, got %r.' % arg)

    ### PUBLIC ATTRIBUTES ###

    @property
    def md5_link(self):
        return HTML.tag('a', href=self.url, c=self.event.md5)

    @property
    def numbered_link(self):
        return HTML.tag('a', href=self.url, c="No.%d" % self.event.id)

    @property
    def url(self):
        return self.request.route_url('single_event', md5=self.event.md5)