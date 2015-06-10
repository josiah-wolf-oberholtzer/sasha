from pyramid.httpexceptions import HTTPFound, HTTPNotFound
from pyramid.view import view_config

from sasha import *
from sashaweb.views._View import _View


@view_config(route_name='random_event')
class RandomEventView(_View):

    def __call__(self):
        return HTTPFound(location=self.location)

    ### PUBLIC ATTRIBUTES ###

    @property
    def location(self):
        md5 = SASHA.get_session( ).query(Event).order_by('RANDOM( )').limit(1)[0].md5
        return self.request.route_url('single_event', md5=md5)
