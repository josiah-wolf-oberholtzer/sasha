from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sasha import domaintools
from sasha import sasha_configuration
from sashaweb.views.View import View


@view_config(route_name='random_event')
class RandomEventView(View):

    ### SPECIAL METHODS ###

    def __call__(self):
        return HTTPFound(location=self.location)

    ### PUBLIC ATTRIBUTES ###

    @property
    def location(self):
        query = sasha_configuration.get_session().query(domaintools.Event)
        query = query.order_by('RANDOM()').limit(1)
        md5 = query[0].md5
        return self.request.route_url('event', md5=md5)