import os
from sasha import SASHACFG
from sasha.core.bootstrap._Fixture import _Fixture


def _get_fixtures( ):

    fixtures = { }

    events_path = os.path.join(SASHACFG.get_media_path('fixtures'), 'events')
    instruments_path = os.path.join(SASHACFG.get_media_path('fixtures'), 'instruments')
    performers_path = os.path.join(SASHACFG.get_media_path('fixtures'), 'performers')
    
    fixtures['events'] = tuple([_Fixture(os.path.join(events_path, filename)) for filename in \
        filter(lambda x: x.endswith('.fixture'), os.listdir(events_path))])

    fixtures['instruments'] = tuple([_Fixture(os.path.join(instruments_path, filename)) for filename in \
        filter(lambda x: x.endswith('.fixture'), os.listdir(instruments_path))])

    fixtures['performers'] = tuple([_Fixture(os.path.join(performers_path, filename)) for filename in \
        filter(lambda x: x.endswith('.fixture'), os.listdir(performers_path))])

    return fixtures
