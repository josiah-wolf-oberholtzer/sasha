import sqlite3
from sasha import SASHACFG
from sasha.core.domain._DomainObject import _DomainObject
from sasha.core.domain.Instrument import Instrument


class Idiom(_DomainObject):

    _table_name = 'idioms'

    _table_sql = '''
        CREATE TABLE idioms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idiom VARCHAR(512) NOT NULL,
            compact_idiom VARCHAR(128) NOT NULL,
            instrument_id INTEGER NOT NULL,
            FOREIGN KEY(instrument_id) REFERENCES instruments(id)
        )
    '''

    __slots__ = ('_compact_idiom', '_ID', '_idiom', '_instrument')

    ### OVERRIDES

    def __repr__(self):
        return '%s(%s, %s)' % (self.__class__.__name__,
            self._idiom, repr(self._instrument.name))

    ### PRIVATE METHODS

    def _init_attributes(self, attrdict):
        object.__setattr__(self, '_compact_idiom', str(attrdict['compact_idiom']))
        object.__setattr__(self, '_ID', int(attrdict['id']))
        object.__setattr__(self, '_idiom',
            tuple([str(x) for x in sorted(filter(None, attrdict['idiom'].split(',')))]))
        object.__setattr__(self, '_instrument', Instrument(attrdict['instrument_id']))

    @staticmethod
    def _levenshtein(s1, s2):
        if len(s1) < len(s2):
            return levenshtein(s2, s1)
        if not s1:
            return len(s2)
        previous_row = xrange(len(s2) + 1)
        for i, c1 in enumerate(s1):
            current_row = [i + 1]
            for j, c2 in enumerate(s2):
                insertions = previous_row[j + 1] + 1
                deletions = current_row[j] + 1       
                substitutions = previous_row[j] + (c1 != c2)
                current_row.append(min(insertions, deletions, substitutions))
            previous_row = current_row
        return previous_row[-1]

#    @classmethod
#    def _parse_new_arg(klass, arg):
#        assert isinstance(arg, int) and 0 < arg
#        return arg

    def _search_by_levenshtein(self, limit):
        assert 0 < limit
        dbc = SASHACFG.get_sqlite3( )
        dbc.create_function('lev', 2, self._levenshtein)
        cur = dbc.cursor( )
        result = cur.execute('SELECT id, lev(?, compact_idiom) FROM idioms \
            WHERE instrument_id == ? ORDER BY lev(?, compact_idiom) LIMIT ?',
            (self.compact_idiom, self.instrument.ID, self.compact_idiom, limit)
            ).fetchall( )
        objects = [(x[1], Idiom(x[0])) for x in result]
        cur.close( )
        dbc.close( )
        return tuple(objects)

    ### PUBLIC ATTRIBUTES

    @property
    def compact_idiom(self):
        return self._compact_idiom

    @property
    def idiom(self):
        return self._idiom

    @property
    def instrument(self):
        return self._instrument

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

    def search(self, method = 'levenshtein', limit = 10):
        assert method in ['levenshtein'] # can add other methods later
        assert 0 < limit
        return self._search_by_levenshtein(limit)
