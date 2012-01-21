import os
from sasha import SASHA
from sasha.core.bootstrap.Fixture import Fixture


def _get_fixtures( ):

    fixtures = { }

    events_path = os.path.join(SASHA.get_media_path('fixtures'), 'events')
    instruments_path = os.path.join(SASHA.get_media_path('fixtures'), 'instruments')
    performers_path = os.path.join(SASHA.get_media_path('fixtures'), 'performers')
    
    fixtures['events'] = tuple([Fixture(os.path.join(events_path, filename)) for filename in \
        filter(lambda x: x.endswith('.fixture'), os.listdir(events_path))])

    fixtures['instruments'] = tuple([Fixture(os.path.join(instruments_path, filename)) for filename in \
        filter(lambda x: x.endswith('.fixture'), os.listdir(instruments_path))])

    fixtures['performers'] = tuple([Fixture(os.path.join(performers_path, filename)) for filename in \
        filter(lambda x: x.endswith('.fixture'), os.listdir(performers_path))])

    return fixtures
