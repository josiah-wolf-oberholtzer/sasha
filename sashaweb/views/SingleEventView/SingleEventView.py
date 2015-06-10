from pyramid.view import view_config
from sasha import *
from sashaweb.views.SearchView import SearchView


@view_config(route_name='single_event', renderer='sashaweb:views/SingleEventView/single_event.mako')
class SingleEventView(SearchView):

    def __init__(self, request):
        self._request = request
        md5 = self.request.matchdict['md5']
        try:
            self._event = Event.get_one(md5=md5)
        except:
            raise HTTPNotFound("SASHA couldn't find an Event linked to <em>%s</em>." % md5)
        self._fingering = self.event.fingering
        self._instrument = self.event.instrument

    ### SPECIAL METHODS ###

    def __call__(self):

        return {
            'body_class': 'search',
            'chroma_events': self.chroma_events,
            'clusters': self.clusters,
            'fingerings': self.fingering.find_similar_fingerings(n=12),
            'instrument_name': self.instrument.name,
            'mfcc_events': self.mfcc_events,
            'page_title': self.page_title, 
            'single_event': self.event,
        }

    ### PUBLIC ATTRIBUTES ###

    @property
    def chroma_events(self):
        adb = AudioDB('chroma')
        events = Event.get(instrument_id=self.instrument.id)
        result = adb.query(self.event, 12, events)
        return [x[1] for x in result]

    @property
    def clusters(self):
        return sasha_configuration.get_session().query(Cluster).join(Event.clusters).filter(Event.id==self.event.id)

    @property
    def event(self):
        return self._event

    @property
    def fingering(self):
        return self._fingering

    @property
    def instrument(self):
        return self._instrument

    @property
    def mfcc_events(self):
        adb = AudioDB('mfcc')
        events = Event.get(instrument_id=self.instrument.id)
        result = adb.query(self.event, 12, events)
        return [x[1] for x in result]

    @property
    def page_title(self):
        return 'SASHA | %s Event: %s' % (self.instrument.name, self.event.md5)

    @property
    def request(self):
        return self._request
