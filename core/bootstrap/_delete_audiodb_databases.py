from sasha import SASHA
from sasha.core.wrappers import AudioDB


def _delete_audiodb_databases( ):

    for name in SASHA['audioDB']:
        adb = AudioDB(name)
        adb.delete( )
