import sqlite3
from sasha import SASHACFG
from sasha.core.domain import *


def _create_sqlite3_database( ):
    
    print 'CREATING SQLITE3 DATABASE:',

    dbc = SASHACFG.get_sqlite3( )
    cur = dbc.cursor( )

    cur.execute('DROP TABLE IF EXISTS events')
    cur.execute('DROP TABLE IF EXISTS idioms')
    cur.execute('DROP TABLE IF EXISTS instruments')
    cur.execute('DROP TABLE IF EXISTS performers')

    cur.execute(Performer._table_sql)
    cur.execute(Instrument._table_sql)
    cur.execute(Idiom._table_sql)
    cur.execute(Event._table_sql)

    dbc.commit( )
    dbc.close( )

    print '...ok!'
