from sasha import SASHACFG
from sasha.core.wrappers import AudioDB


def _create_audiodb_databases( ):

    print 'CREATING AUDIODB DATABASES:'

    for name in SASHACFG['audioDB']:
       print '\tCREATING %s:' % name,
       adb = AudioDB(name)
       adb.create( )
       print '...ok!'
