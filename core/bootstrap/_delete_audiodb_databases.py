from sasha import *
from sasha.core.wrappers import AudioDB


def _delete_audiodb_databases( ):

    SASHA.logger.info('Deleting audioDB databases.')

    for name in SASHA['audioDB']:
        AudioDB(name).delete( )
