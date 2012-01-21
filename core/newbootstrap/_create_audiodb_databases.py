from sasha import *


def _create_audiodb_databases( ):

    SASHA.logger.info('Creating audioDB databases.')

    for name in SASHA['audioDB']:
       adb = AudioDB(name)
       adb.create( )
