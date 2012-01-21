from sasha import *


def _delete_audiodb_databases( ):

    SASHA.logger.info('Deleting audioDB databases.')

    for name in SASHA['audioDB']:
        adb = AudioDB(name)
        adb.delete( )
