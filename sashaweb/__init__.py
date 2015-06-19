from pyramid.config import Configurator
from pyramid.httpexceptions import HTTPNotFound
from pyramid.session import UnencryptedCookieSessionFactoryConfig
from sashaweb.views import *


def includeme(config):
    config.include('pyramid_mako')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('assets/mp3s', 'sashamedia:development/mp3s/', cache_max_age=3600)
    config.add_static_view('assets/plots', 'sashamedia:development/plots/', cache_max_age=3600)
    config.add_static_view('assets/scores', 'sashamedia:development/scores/', cache_max_age=3600)
    config.add_static_view('docs', 'sasha:docs/build/html/', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('help', '/help/')
    config.add_route('all_clusters', '/clusters/')
    config.add_route('single_cluster', '/clusters/{feature}/{cluster_id}/')
    config.add_route('random_event', '/random/')
    config.add_route('search', '/search/')
    config.add_route('single_event', '/events/{md5}/')
    config.add_route('single_instrument', '/instruments/{instrument_name}/')
    config.add_route('single_fingering', '/instruments/{instrument_name}/{compact_representation}/')
    config.scan('sashaweb.views')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = UnencryptedCookieSessionFactoryConfig('hobbeshobbertson')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.include(includeme)
    return config.make_wsgi_app()