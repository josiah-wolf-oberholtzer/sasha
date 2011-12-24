import os
import sqlite3
import subprocess
from abjad.tools.pitchtools import NumberedChromaticPitch
from abjad.tools.pitchtools import NumberedChromaticPitchClass
from sasha import SASHACFG
from sasha.core.domain._DomainObject import _DomainObject
from sasha.core.domain.Idiom import Idiom
from sasha.core.domain.Instrument import Instrument
from sasha.core.domain.Performer import Performer
from sasha.core.wrappers import AudioDB
from sasha.core.wrappers import Playback


class Event(_DomainObject):

    _table_name = 'events'

    _table_sql = '''
        CREATE TABLE events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name UNIQUE NOT NULL,
            instrument_id INTEGER NOT NULL,
            performer_id INTEGER NOT NULL,
            idiom_id INTEGER NOT NULL,
            md5 VARCHAR(32) NOT NULL,
            FOREIGN KEY (instrument_id) REFERENCES instruments(id),
            FOREIGN KEY (performer_id) REFERENCES performers(id),
            FOREIGN KEY (idiom_id) REFERENCES idioms(id)
        )
   '''

    __slots__ = ('_ID', '_idiom', '_instrument', '_md5', '_name', '_performer')

    ### PRIVATE METHODS ###

    @classmethod
    def _get_id_from_md5(md5):
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM events WHERE md5 == ?',
            (md5,)).fetchall( )
        if not result:
            raise ValueError("No Event with name '%s'" % md5)
        cur.close( )
        dbc.close( )
        return result[0][0]

    @classmethod
    def _get_id_from_name(name):
        dbc = SASHACFG.get_sqlite3( )
        cur = dbc.cursor( )
        result = cur.execute('SELECT id FROM events WHERE name == ?',
            (name,)).fetchall( )
        if not result:
            raise ValueError("No Event with name '%s'" % name)
        cur.close( )
        dbc.close( )
        return result[0][0]

    @classmethod
    def _get_id_from_string(klass, string):
        if string.startswith('md5:'):
            return klass._get_id_from_md5(string[4:])
        return klass._get_id_from_string(string)

    def _init_attributes(self, attrdict):
        object.__setattr__(self, '_ID', int(attrdict['id']))
        object.__setattr__(self, '_md5', str(attrdict['md5']))
        object.__setattr__(self, '_name', str(attrdict['name']))
        object.__setattr__(self, '_instrument', Instrument(attrdict['instrument_id']))
        object.__setattr__(self, '_performer', Performer(attrdict['performer_id']))
        object.__setattr__(self, '_idiom', Idiom(attrdict['idiom_id']))

    def _search_by_levenshtein(self, limit):
        assert isinstance(limit, int) and 0 < limit
        results = self.idiom.search('levenshtein', limit + 1)
        print results
        events = [ ]
        for distance, idiom in results:
            idiom_events = idiom.get_referencing_events( )
            for idiom_event in idiom_events:
                if idiom_event != self:
                    events.append((distance, idiom_event))
        return tuple(events[:limit])

    ### PUBLIC PROPERTIES ###

    @property
    def idiom(self):
        return self._idiom

    @property
    def instrument(self):
        return self._instrument

    @property
    def md5(self):
        return self._md5

    @property
    def performer(self):
        return self._performer

    ### PUBLIC METHODS

    @staticmethod
    def filter_by_idiom(instrument, idiom_dict):
        assert isinstance(idiom_dict, dict)
        instrument = Instrument(instrument)
        events = instrument.get_referencing_events( )
        for key in idiom_dict:
            assert key in instrument.idiom_schema
            if idiom_dict[key]:
                events = filter(lambda x: key in x.idiom.idiom, events)                
            else:
                events = filter(lambda x: key not in x.idiom.idiom, events)
        return events

    @staticmethod
    def filter_by_pitches(pitch_dict):
        from sasha.plugins import ChordAnalysis
        assert isinstance(pitch_dict, dict)

        # convert to float, prune enharmonics
        new_dict = { }
        for key, value in pitch_dict.iteritems( ):
            new_dict[float(NumberedChromaticPitch(key))] = value
        
        chords = [ChordAnalysis(x) for x in Event.get_all( )]
        for chord in chords:
            result = chord.read( )

        for pitch in new_dict:
            if new_dict[pitch]:
                chords = filter(lambda x: pitch in x.pitches, chords)
            else:
                events = filter(lambda x: pitch not in x.pitches, chords)

        return tuple([x.event for x in chords])

    @staticmethod
    def filter_by_pitch_classes(pitch_class_dict):
        from sasha.plugins import ChordAnalysis
        assert isinstance(pitch_class_dict, dict)

        chords = [ChordAnalysis(x) for x in Event.get_all( )]
        for chord in chords:
            result = chord.read( )

        # convert to float, prune enharmonics
        new_dict = { }
        for key, value in pitch_class_dict.iteritems( ):
            new_dict[float(NumberedChromaticPitchClass(key))] = value

        for pitch_class in new_dict:
            if new_dict[pitch_class]:
                chords = filter(lambda x: pitch_class in x.pitch_classes, chords)
            else:
                chords = filter(lambda x: pitch_class not in x.pitch_classes, chords)

        return tuple([x.event for x in chords])

    def playback(self):
        from sasha.plugins import SourceAudio
        Playback( )(SourceAudio(self).path)

    def search(self, method, limit = 10):
        assert isinstance(limit, int) and 0 < limit
        if method in SASHACFG['audioDB']:
            adb = AudioDB(method)
            return adb.query(self, limit)
        elif method in ['lev', 'levenshtein']:
            return self._search_by_levenshtein(limit)
        else:
            raise ValueError('Unknown search method "%s".' % repr(method))

