from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

from sasha import SASHACFG
from sasha.core.sqldomain import *


def _bootstrap( ):

    dbpath = os.path.join(SASHACFG.get_media_path('databases'),
        SASHACFG['sqlite3']['sqlalchemy'])    

    engine = create_engine('sqlite://%s' % dbpath)

