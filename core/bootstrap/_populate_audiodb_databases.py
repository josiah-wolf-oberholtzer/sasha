from sasha import *


def _populate_audiodb_databases( ):

    SASHA.logger.info('Populating audioDB databases.')

    events = Event.get( )
    assert 0 < len(events)
    for name in SASHA['audioDB']:
        adb = AudioDB(name)
        adb.populate(events)
