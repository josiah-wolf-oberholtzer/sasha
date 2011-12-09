import sqlite3
from sasha import SASHACFG
from sasha.core.domain._DomainObject import _DomainObject


class Instrument(_DomainObject):

    _table_name = 'instruments'

    _table_sql = '''
        CREATE TABLE instruments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(128) UNIQUE NOT NULL,
            idiom_schema VARCHAR(512),
            parent_id INTEGER,
            FOREIGN KEY(parent_id) REFERENCES instruments(id)
        )
    '''

    __slots__ = ('_ID', '_idiom_schema', '_name', '_parent')

    ### PRIVATE METHODS ###

    def _init_attributes(self, attrdict):
        object.__setattr__(self, '_ID', int(attrdict['id']))
        object.__setattr__(self, '_name', str(attrdict['name']))
        if attrdict['idiom_schema'] is not None:
            object.__setattr__(self, '_idiom_schema',
                tuple([str(x) for x in sorted(filter(None, attrdict['idiom_schema'].split(',')))]))
        else:
            object.__setattr__(self, '_idiom_schema', None)
        if attrdict['parent_id'] is not None:
            object.__setattr__(self, '_parent', Instrument(attrdict['parent_id']))
        else:
            object.__setattr__(self, '_parent', None)

    ### PUBLIC ATTRIBUTES ###   

    @property
    def idiom_schema(self):
        if self._idiom_schema is not None:
            return tuple(self._idiom_schema)
        return self._idiom_schema

    @property
    def children(self):
        def recurse(ID):
            children = [ ]
            dbc = SASHACFG.get_sqlite3( )
            cur = dbc.cursor( )
            results = cur.execute('SELECT id FROM instruments WHERE parent_id == ?',
                (ID,)).fetchall( )
            cur.close( )
            dbc.close( )
            for result in results:
                child = Instrument(result[0])
                children.append(child)
                children.extend(recurse(child.ID))
            return children
        return recurse(self.ID)

    @property
    def parent(self):
        return self._parent

    ### PUBLIC METHODS ###

    def get_filtered_referencing_idioms(self, filter_dict = { }):
        assert isinstance(filter_dict, dict)
        idioms = self.get_referencing_idioms( )
        for key, value in filter_dict.iteritems( ):
            if not key in self.idiom_schema:
                continue
            if value:
                idioms = filter(lambda x: key in x.idiom, idioms)
            else:
                idioms = filter(lambda x: key not in x.idiom, idioms)
        return idioms

    def get_count_of_referencing_events(self):
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT COUNT(*) FROM events WHERE instrument_id == ?',
            (self.ID,)).fetchall( )
        cur.close( )
        dbc.close( )
        return result[0][0]

    def get_count_of_child_referencing_events(self):
        count = 0
        instruments = [self]
        instruments.extend(self.children)
        for instrument in instruments:
            count += instrument.get_count_of_referencing_events( )
        return count

    def get_referencing_events(self):
        from sasha.core.domain.Event import Event 
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM events WHERE instrument_id == ?',
            (self.ID,)).fetchall( )   
        cur.close( )
        dbc.close( )
        return tuple([Event(x[0]) for x in result])

    def get_child_referencing_events(self):
        events = [ ]
        instruments = [self]
        instruments.extend(self.children)
        for instrument in instruments:
            events.extend(instrument.get_referencing_events( ))
        return events

    def get_referencing_idioms(self):
        from sasha.core.domain.Idiom import Idiom
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM idioms WHERE instrument_id == ?',
            (self.ID,)).fetchall( )   
        cur.close( )
        dbc.close( )
        return tuple([Idiom(x[0]) for x in result])
