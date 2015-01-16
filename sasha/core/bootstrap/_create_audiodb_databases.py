from sasha import *
from sasha.core.wrappers import AudioDB


def _create_audiodb_databases():

    SASHA.logger.info('Creating audioDB databases.')

    for name in SASHA['audioDB']:
       AudioDB(name).create()
