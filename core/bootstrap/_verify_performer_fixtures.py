import os
from sasha import SASHACFG
from sasha.core.bootstrap._Fixture import _Fixture
from sasha.core.exceptions import MalformedFixtureError


def _verify_performer_fixtures( ):
    print 'VERIFYING PERFORMER FIXTURES:'

    path = os.path.join(SASHACFG.get_media_path('fixtures'), 'performers')
    for file in filter(lambda x: x.endswith('.fixture'), os.listdir(path)):
        fullpath = os.path.join(path, file)

        print '\t%s:' % fullpath,

        fixture = _Fixture(fullpath)

        errors = [ ]

        if 'name' not in fixture['main']:
            errors.append("Performer fixture requires a 'name' option.")
        elif not fixture['main']['name']:
            errors.append("Performer fixture require a non-zero-length 'name' value.")

        if errors:
            errors.insert(0, '%s:' % fullpath)
            raise MalformedFixtureError('\n\t' + '\n\t'.join(errors))

        print '...ok!'
