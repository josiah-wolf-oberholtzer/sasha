import sqlite3
from sasha import SASHACFG
from sasha.core.domain._DomainObject import _DomainObject


class Performer(_DomainObject):

    _table_name = 'performers'

    _table_sql = '''
        CREATE TABLE performers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(128) UNIQUE NOT NULL
        )
    '''
            
    __slots__ = ('_ID', '_name')
            
    ### PRIVATE METHODS

    def _init_attributes(self, attrdict):
        object.__setattr__(self, '_ID', int(attrdict['id']))
        object.__setattr__(self, '_name', str(attrdict['name']))

    ### PUBLIC METHODS

    def get_referencing_events(self):
        from sasha.core.domain.Event import Event 
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM events WHERE idiom_id == ?',
            (self.ID,)).fetchall( )   
        cur.close( )
        dbc.close( )
        return tuple([Event(x[0]) for x in result])
