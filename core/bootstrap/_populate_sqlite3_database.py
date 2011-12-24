import sqlite3
from sasha import SASHACFG
from sasha import Event
from sasha.plugins import SourceAudio
from sasha.core.bootstrap._get_fixtures import _get_fixtures


def _populate_sqlite3_database( ):

    print 'POPULATING SQLITE3 DATABASE:',

    dbc = SASHACFG.get_sqlite3( )
    cur = dbc.cursor( )

    fixtures = _get_fixtures( )  

    # insert performers
    for performer in fixtures['performers']:
        cur.execute("INSERT INTO performers(name) VALUES(?)",
            (performer['main']['name'],))

    # insert instrument names (without parent_ids)
    for instrument in fixtures['instruments']:
        if instrument['main']['idiom_schema']:
            idiom_schema = ','.join(sorted(instrument['main']['idiom_schema'].split(' ')))
            cur.execute("INSERT INTO instruments(idiom_schema, name) VALUES(?, ?)",
                (idiom_schema, instrument['main']['name']))
        else:
            cur.execute("INSERT INTO instruments(name) VALUES(?)",
                (instrument['main']['name'],))

    # then update instrument records with parent_ids (to insure integrity)
    for instrument in fixtures['instruments']:
        if instrument['main']['parent_name']:
            query = cur.execute("SELECT id FROM instruments WHERE name == ?",
                (instrument['main']['parent_name'],))
            parent_id = query.next( )[0]
            cur.execute("UPDATE instruments SET parent_id = ? WHERE name == ?",
                (parent_id, instrument['main']['name']))

    # insert events and idioms
    for event in fixtures['events']:

        # get instrument and performer ids, and idiom_schema
        result = cur.execute("SELECT id, idiom_schema FROM instruments WHERE name == ?",
            (event['main']['instrument_name'],)).fetchall( )
        instrument_id, idiom_schema = result[0][0], result[0][1].split(',')
        result = cur.execute("SELECT id FROM performers WHERE name == ?",
            (event['main']['performer_name'],))
        performer_id = result.next( )[0]

        # insert idiom row
        idiom_string = ','.join(sorted(event['main']['idiom'].split(' ')))
        compact_idiom = ''
        for key in idiom_schema:
            if key in event['main']['idiom']:
                compact_idiom += '1'
            else:
                compact_idiom += '0'
        result = cur.execute("SELECT * FROM idioms WHERE idiom == ? AND instrument_id == ?",
            (idiom_string, instrument_id,)).fetchall( )
        if not len(result):
            cur.execute("INSERT INTO idioms(compact_idiom, idiom, instrument_id) VALUES(?, ?, ?)",
                (compact_idiom, idiom_string, instrument_id,))

        # get idiom id
        idiom_id = cur.execute("SELECT id FROM idioms WHERE idiom == ? AND instrument_id == ?",
            (idiom_string, instrument_id,)).fetchall( )[0][0]
        
        # insert event row
        cur.execute("INSERT INTO events(name, idiom_id, instrument_id, performer_id) VALUES(?, ?, ?, ?)",
            (event['main']['name'], idiom_id, instrument_id, performer_id))

    print '...ok!'

    dbc.commit( )

    # now that events are populated, update with md5 information
    for x in Event.get_all( ):
        ID = x.ID
        md5 = SourceAudio(ID).md5
        print ID, md5
        cur.execute("UPDATE events SET md5 = ? WHERE id == ?", (md5, ID))

    dbc.commit( )
    dbc.close( )
