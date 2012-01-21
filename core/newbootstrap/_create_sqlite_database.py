import os

from sqlalchemy import create_engine

from sasha import *


def _create_sqlite_database( ):

    SASHA.logger.info('Creating empty SQLite database.')

    dbpath = os.path.join(SASHA.get_media_path('databases'),
        SASHA['sqlite']['sqlite'])
    engine = create_engine('sqlite:///%s' % dbpath)
    metadata = Event.metadata
    metadata.drop_all(engine)
    metadata.create_all(engine)
