from sasha import SASHACFG
from sasha import Event
from sasha.core.wrappers import AudioDB


def _populate_audiodb_databases( ):
        
    print 'POPULATING AUDIODB DATABASES:'

    events = Event.get_all( )
    for name in SASHACFG['audioDB']:
       print '\tPOPULATING %s:' % name,
       adb = AudioDB(name)
       adb.populate(events)
       print '...ok!'
