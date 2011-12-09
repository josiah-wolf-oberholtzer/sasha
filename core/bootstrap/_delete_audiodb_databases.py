from sasha import SASHACFG
from sasha.core.wrappers import AudioDB


def _delete_audiodb_databases( ):

    for name in SASHACFG['audioDB']:
        adb = AudioDB(name)
        adb.delete( )
