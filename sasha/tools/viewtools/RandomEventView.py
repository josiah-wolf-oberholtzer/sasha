import random
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sasha.tools import modeltools
from sasha.tools.viewtools.View import View


@view_config(route_name='random_event')
class RandomEventView(View):

    ### SPECIAL METHODS ###

    def __call__(self):
        return HTTPFound(location=self.location)

    ### PUBLIC ATTRIBUTES ###

    @property
    def location(self):
        event_count = modeltools.Event.objects.count()
        event_index = random.randrange(event_count)
        event = modeltools.Event.objects[event_index]
        return self.request.route_url('event', md5=event.md5)