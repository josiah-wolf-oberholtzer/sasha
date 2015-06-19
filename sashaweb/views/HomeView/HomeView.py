from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from sasha import *
from sashaweb.views._View import _View


#@view_config(route_name='home', renderer='sashaweb:templates/home.mako')
@view_config(route_name='home')
class HomeView(_View):

    def __call__(self):
        return HTTPFound(location=self.location)

    ### PUBLIC ATTRIBUTES ###

    @property
    def location(self):
        return self.request.route_url('search')