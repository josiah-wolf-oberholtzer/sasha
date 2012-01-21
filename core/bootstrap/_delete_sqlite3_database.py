import os
from sasha import SASHA


def _delete_sqlite3_database( ):
    
    path = os.path.join(SASHA.get_media_path('databases'),
        SASHA['sqlite3']['sqlite3'])
    if os.path.exists(path):
        os.remove(path)
