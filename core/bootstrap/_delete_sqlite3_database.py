import os
from sasha import SASHACFG


def _delete_sqlite3_database( ):
    
    path = os.path.join(SASHACFG.get_media_path('databases'),
        SASHACFG['sqlite3']['sqlite3'])
    if os.path.exists(path):
        os.remove(path)
