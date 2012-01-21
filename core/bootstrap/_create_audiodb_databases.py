from sasha import SASHA
from sasha.core.wrappers import AudioDB


def _create_audiodb_databases( ):

    print 'CREATING AUDIODB DATABASES:'

    for name in SASHA['audioDB']:
       print '\tCREATING %s:' % name,
       adb = AudioDB(name)
       adb.create( )
       print '...ok!'
