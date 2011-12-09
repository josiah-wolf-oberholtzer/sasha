import os
from sasha import SASHACFG
from sasha.core.bootstrap._Fixture import _Fixture
from sasha.core.exceptions import MalformedFixtureError


def _verify_instrument_fixtures( ):
    print 'VERIFYING INSTRUMENT FIXTURES:'

    path = os.path.join(SASHACFG.get_media_path('fixtures'), 'instruments')

    for file in filter(lambda x: x.endswith('.fixture'), os.listdir(path)):
        fullpath = os.path.join(path, file)

        print '\t%s:' % fullpath,

        fixture = _Fixture(fullpath)

        errors = [ ]

        if 'idiom_schema' not in fixture['main']:
            errors.append("Instrument fixture requires an 'idiom_schema' option.")

        if 'name' not in fixture['main']:
            errors.append("Instrument fixture requires a 'name' option.")
        elif not fixture['main']['name']:
            errors.append("Instrument fixture requires a non-zero-length 'name' option.")

        if 'parent_name' not in fixture['main']:
            errors.append("Instrument fixture requires a 'parent_name' option.")

        if errors:
            errors.insert(0, '%s:' % fullpath)
            raise MalformedFixtureError('\n\t' + '\n\t'.join(errors))

        print '...ok!'
