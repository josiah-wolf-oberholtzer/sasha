from pyramid.httpexceptions import HTTPNotFound
from pyramid.view import view_config
from sasha.views.SearchView import SearchView
from sasha.tools import executabletools
from sasha.tools import newdomaintools


@view_config(
    route_name='event',
    renderer='sasha:templates/event.mako',
    )
class EventView(SearchView):

    ### INITIALIZER ###

    def __init__(self, request):
        self._request = request
        md5 = self.request.matchdict['md5']
        try:
            self._event = newdomaintools.Event.objects.get(md5=md5)
        except:
            message = "SASHA couldn't find an Event linked to <em>{}</em>."
            message = message.format(md5)
            raise HTTPNotFound(message)

    ### SPECIAL METHODS ###

    def __call__(self):
        return {
            'body_class': 'search',
            'chroma_events': self.chroma_events,
            'clusters': self.event.clusters,
            'current_event': self.event,
            'fingerings': self.event.fingering.find_similar_fingerings(n=12),
            'current_instrument': self.event.fingering.instrument,
            'mfcc_events': self.mfcc_events,
            'title': self.title,
            }

    ### PUBLIC ATTRIBUTES ###

    @property
    def chroma_events(self):
        adb = executabletools.AudioDB('chroma')
        events = newdomaintools.Event.objects(
            fingering__instrument=self.event.fingering.instrument,
            )
        result = adb.query(self.event, 12, events)
        return [x[1] for x in result]

    @property
    def event(self):
        return self._event

    @property
    def mfcc_events(self):
        adb = executabletools.AudioDB('mfcc')
        events = newdomaintools.Event.objects(
            fingering__instrument=self.event.fingering.instrument,
            )
        result = adb.query(self.event, 12, events)
        return [x[1] for x in result]

    @property
    def title(self):
        return 'SASHA | {} Event: {}'.format(
            self.event.fingering.instrument.name,
            self.event.md5,
            )

    @property
    def request(self):
        return self._request