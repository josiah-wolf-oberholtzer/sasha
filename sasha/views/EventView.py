from pyramid.view import view_config
from sasha import *
from sasha.views.SearchView import SearchView


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
            self._event = Event.get_one(md5=md5)
        except:
            message = "SASHA couldn't find an Event linked to <em>{}</em>."
            message = message.format(md5)
            raise HTTPNotFound(message)
        self._fingering = self.event.fingering
        self._instrument = self.event.instrument

    ### SPECIAL METHODS ###

    def __call__(self):
        return {
            'body_class': 'search',
            'chroma_events': self.chroma_events,
            'clusters': self.clusters,
            'current_event': self.event,
            'fingerings': self.fingering.find_similar_fingerings(n=12),
            'current_instrument': self.instrument,
            'mfcc_events': self.mfcc_events,
            'title': self.title,
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
        query = sasha_configuration.get_session().query(Cluster)
        query = query.join(Event.clusters).filter(Event.id==self.event.id)
        return query

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
    def title(self):
        return 'SASHA | %s Event: %s' % (self.instrument.name, self.event.md5)

    @property
    def request(self):
        return self._request