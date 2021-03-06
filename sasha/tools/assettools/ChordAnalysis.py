import cPickle
import os
from abjad.tools import pitchtools
from sasha.tools.assettools.Asset import Asset
from sasha.tools.assettools.PartialTrackingAnalysis import PartialTrackingAnalysis


class ChordAnalysis(Asset):

    ### CLASS VARIABLES ###

    __requires__ = PartialTrackingAnalysis
    __slots__ = (
        '_asset',
        '_client',
        '_pitches',
        '_pitch_classes',
        )
    file_suffix = 'chord'
    media_type = 'analyses'

    ### INITIALIZER ###

    def __init__(self, arg):
        Asset.__init__(self, arg)
        self._pitches = None
        self._pitch_classes = None

    ### PRIVATE METHODS ###

    def _find_chord(self):
        pta = PartialTrackingAnalysis(self)
        tracks = pta.read()
        if not tracks:
            message = 'Cannot find any partial tracks for {!r}'
            message = message.format(self.client.name)
            raise Exception(message)
        db_threshold = -7
        tracks = [_ for _ in tracks if 100 < len(_)]
        tracks = sorted(tracks, key=lambda x: x.amplitude_mean, reverse=True)
        tracks = [_ for _ in tracks if db_threshold < _.db(tracks[0])]
        tracks = tuple(tracks)
        semitones = [x.semitones_centroid for x in tracks]
        amplitudes = [x.db(tracks[0].amplitude_mean) for x in tracks]
        zipped = zip(semitones, amplitudes)
        chord_dict = {}
        for pair in zipped:
            pitch, amplitude = pair
            if pitch not in chord_dict:
                chord_dict[pitch] = amplitude
            elif chord_dict[pitch] < amplitude:
                chord_dict[pitch] = amplitude
        return tuple(
            sorted(((k, v) for k, v in chord_dict.iteritems()),
            key=lambda x: x[0]),
            )

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def read(self):
        if self.exists:
            with open(self.path, 'rb') as file_pointer:
                self._asset = cPickle.load(file_pointer)
            pitches = [pitchtools.NumberedPitch(x[0]) for x in self.asset]
            pitch_classes = [pitchtools.NumberedPitchClass(float(x)) for x in pitches]
            self._pitches = tuple(float(_) for _ in pitches)
            self._pitch_classes = tuple(float(_) for _ in pitch_classes)
            return self.asset
        message = 'Asset does not exist for event {}.'
        message = message.format(self.event.name)
        raise Exception(message)

    def write(self, **kwargs):
        self._asset = self._find_chord()
        self.delete()
        with open(self.path, 'wb') as file_pointer:
            cPickle.dump(self.asset, file_pointer)

    ### PUBLIC PROPERTIES ###

    @property
    def pitch_names(self):
        return tuple([str(pitchtools.NamedPitch(x)) for x in self.pitches])

    @property
    def pitches(self):
        return self._pitches

    @property
    def pitch_class_names(self):
        return tuple(set(
            str(pitchtools.NamedPitchClass(x))
            for x in self.pitch_classes
            ))

    @property
    def pitch_classes(self):
        return self._pitch_classes