from sasha.tools.systemtools import SashaConfiguration
sasha_configuration = SashaConfiguration()
del SashaConfiguration

from sasha.tools import *
from sasha.tools.models import *
from sasha.tools.executabletools import AudioDB
del tools

from pyramid.config import Configurator
from pyramid.session import UnencryptedCookieSessionFactoryConfig


def includeme(config):
    config.include('pyramid_mako')
    config.add_route('cluster', '/clusters/{feature}/{cluster_id}/')
    config.add_route('event', '/events/{md5}/')
    config.add_route('fingering', '/instruments/{instrument_name}/{compact_representation}/')
    config.add_route('help', '/help/')
    config.add_route('home', '/')
    config.add_route('instrument', '/instruments/{instrument_name}/')
    config.add_route('random_event', '/random/')
    config.add_route('search', '/search/')
    config.add_static_view(
        'assets/mp3s',
        'sashamedia:{}/mp3s/'.format(sasha_configuration.environment),
        cache_max_age=3600,
        )
    config.add_static_view(
        'assets/plots',
        'sashamedia:{}/plots/'.format(sasha_configuration.environment),
        cache_max_age=3600,
        )
    config.add_static_view(
        'assets/scores',
        'sashamedia:{}/scores/'.format(sasha_configuration.environment),
        cache_max_age=3600,
        )
    config.add_static_view('docs', 'sasha:docs/build/html/', cache_max_age=3600)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan('sasha.views')


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    session_factory = UnencryptedCookieSessionFactoryConfig('hobbeshobbertson')
    config = Configurator(settings=settings, session_factory=session_factory)
    config.include(includeme)
    return config.make_wsgi_app()