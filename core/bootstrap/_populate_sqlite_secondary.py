from abjad.tools.pitchtools import NamedChromaticPitch

from sasha import *
from sasha.plugins import ChordAnalysis


def _populate_sqlite_secondary( )

    SASHA.logger.info('Populate SQLite secondary objects.')

    session = SASHA.get_session( )

    for event in Event.get( ):
        chord = ChordAnalysis(event).read( )
        for pitch_number, amplitude in chord:
            pitch = NamedChromaticPitch(pitch_number)
            pitch_class_number = pitch.chromatic_pitch_class_number
            octave_number = pitch.octave_number
            session.add(Partial(event=event,
                pitch_number=pitch_number,
                pitch_class_number=pitch_class_number,
                octave_number=octave_number

    session.commit( )
