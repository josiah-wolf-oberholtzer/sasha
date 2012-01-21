import os
from sasha import SASHACFG
from sasha import SASHAROOT
from sasha.core.bootstrap.Fixture import Fixture
from sasha.core.exceptions import MalformedFixtureError


def _verify_event_fixtures( ):
    print 'VERIFYING EVENT FIXTURES:'

    path = os.path.join(SASHACFG.get_media_path('fixtures'), 'events')

    for file in filter(lambda x: x.endswith('.fixture'), os.listdir(path)):
        fullpath = os.path.join(path, file)

        print '\t%s:' % fullpath,

        fixture = Fixture(fullpath)

        errors = [ ]

        if 'idiom' not in fixture['main']:
            errors.append("Event fixture requires an 'idiom' option.")

        if 'instrument_name' not in fixture['main']:
            errors.append("Event fixture requires an 'instrument_name' option.")
        elif not fixture['main']['instrument_name']:
            errors.append("Event fixture requires a non-zero-length 'instrument_name' value.")

        if 'name' not in fixture['main']:
            errors.append("Event fixture requires a 'name' option.")
        elif not fixture['main']['name']:
            errors.append("Event fixture requires a non-zero-length 'name' value.")
        elif fixture['main']['name'] != file.partition('.fixture')[0]:
            errors.append("Event fixture's 'name' value does not match fixture's filename.")

        if 'performer_name' not in fixture['main']:
            errors.append("Event fixture requires a 'performer_name' option.")
        elif not fixture['main']['performer_name']:
            errors.append("Event fixture requires a non-zero-length 'performer_name' value.")

        if errors:
            errors.insert(0, '%s:' % fullpath)
            raise MalformedFixtureError('\n\t' + '\n\t'.join(errors))

        print '...ok!'
