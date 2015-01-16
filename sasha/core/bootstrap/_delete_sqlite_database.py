import os

from sasha import *


def _delete_sqlite_database():

    SASHA.logger.info('Deleting sqlite database.')

    path = os.path.join(SASHA.get_media_path('databases'),
        SASHA['sqlite']['sqlite'])
    if os.path.exists(path):
        os.remove(path)
