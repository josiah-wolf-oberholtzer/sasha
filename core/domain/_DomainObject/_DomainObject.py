import sqlite3
from sasha import SASHACFG
from sasha.core.mixins import _Immutable
from sasha.core.domain import _identity_map


class _DomainObject(_Immutable):

    _table_name = ''

    def __new__(klass, arg):

        # get ID  
        ID = klass._parse_new_arg(arg)

        # check identity map
        if klass not in _identity_map or ID not in _identity_map[klass]:
            self = object.__new__(klass)

            # query db
            dbc = SASHACFG.get_sqlite3( )
            cur = dbc.cursor( )
            result = cur.execute('SELECT * FROM %s WHERE id == ?' % klass._table_name,
                (ID,)).fetchall( )
            if not result:
                raise ValueError("No %s with ID '%d'" % (klass.__name__, ID))

            # set attributes
            row = result[0]
            description = tuple([x[0] for x in cur.description])
            attrdict = { }
            for pair in zip(description, row):
                attrdict[pair[0]] = pair[1]
            self._init_attributes(attrdict)

            # close db
            cur.close( )
            dbc.close( )

            # add to identity map and return
            if klass not in _identity_map:
                _identity_map[klass] = { }
            _identity_map[klass][ID] = self
            return self

        else:
            return _identity_map[klass][ID]

    def __getnewargs__(self):
        return (self.ID,)

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.name))

    ### PRIVATE METHODS ###

    @classmethod
    def _get_id_from_name(klass, name):
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM %s WHERE name == ?' % klass._table_name,
            (name,)).fetchall( )
        if not result:
            raise ValueError("No %s with name '%s'" % (klass.__name__, arg))
        cur.close( )
        dbc.close( )
        return result[0][0]

    @classmethod
    def _get_id_from_string(klass, string):
        return klass._get_id_from_string(string)

    def _init_attributes(self, attrdict):
        raise Exception('Not implemented in %s' % self.__class__.__name__)

    @classmethod
    def _parse_new_arg(klass, arg):
        if isinstance(arg, klass):
            return arg.ID
        elif hasattr(arg, klass.__name__.lower( )):
            return getattr(arg, klass.__name__.lower( )).ID
        elif isinstance(arg, int):
            return arg
        elif isinstance(arg, str):
            return klass._get_id_from_string(arg)
        else:
            raise ValueError('Cannot instantiate %s from argument %s.' % (klass.__name__, arg))

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return self._name

    @property
    def ID(self):
        return self._ID

    ### PUBLIC METHODS

    @classmethod
    def get_all(klass):
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM %s' % klass._table_name).fetchall( )
        objects = tuple([klass(x[0]) for x in result])
        cur.close( )
        dbc.close( )
        return objects

    @classmethod
    def get_random(klass, n = 1):
        assert 0 < n
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM %s ORDER BY RANDOM( ) LIMIT %d' \
            % (klass._table_name, int(n))).fetchall( )
        objects = tuple([klass(x[0]) for x in result])
        cur.close( )
        dbc.close( )
        return objects
