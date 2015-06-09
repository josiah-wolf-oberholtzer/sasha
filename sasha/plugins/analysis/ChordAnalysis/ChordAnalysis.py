import cPickle
import os
from abjad.tools import pitchtools
from sasha.tools.assettools._MediaPlugin import _MediaPlugin
from sasha.plugins.analysis.PartialTrackingAnalysis import PartialTrackingAnalysis


class ChordAnalysis(_MediaPlugin):

    __requires__ = PartialTrackingAnalysis
    __slots__ = ('_asset', '_client', '_pitches', '_pitch_classes',)

    media_type = 'analyses'
    file_suffix = 'chord'

    def __init__(self, arg):
        _MediaPlugin.__init__(self, arg)
        object.__setattr__(self, '_pitches', None)
        object.__setattr__(self, '_pitch_classes', None)

    ### PRIVATE METHODS ###

    def _find_chord(self):
        pta = PartialTrackingAnalysis(self)
        tracks = pta.read()   
        if not tracks:
            raise Exception('Cannot find any partial tracks for "%s"' % self.client.name)
    
        db_threshold = -7

        tracks = filter(lambda x: 100 < len(x), tracks)
        tracks = sorted(tracks, key = lambda x: x.amplitude_mean, reverse = True)
        tracks = filter(lambda x: db_threshold < x.db(tracks[0]), tracks)
        semitones = [x.semitones_centroid for x in tracks]
        amplitudes = [x.db(tracks[0].amplitude_mean) for x in tracks]

        zipped = zip(semitones, amplitudes)
        
        chord_dict = { }
        for pair in zipped:
            pitch, amplitude = pair
            if pitch not in chord_dict:
                chord_dict[pitch] = amplitude
            elif chord_dict[pitch] < amplitude:
                chord_dict[pitch] = amplitude

        return tuple(sorted([(k, v) for k, v in chord_dict.iteritems()], key = lambda x: x[0]))

    ### PUBLIC ATTRIBUTES ###

    @property
    def pitch_names(self):
        return tuple([str(pitchtools.NamedPitch(x)) for x in self.pitches])

    @property
    def pitches(self):
        return self._pitches

    @property
    def pitch_class_names(self):
        return tuple(set([str(pitchtools.NamedPitchClass(x)) for x in self.pitch_classes]))

    @property
    def pitch_classes(self):
        return self._pitch_classes

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def read(self):
        if self.exists:
            input = open(self.path, 'rb')
            object.__setattr__(self, '_asset', cPickle.load(input))
            input.close()
            pitches = [pitchtools.NumberedPitch(x[0]) for x in self.asset]
            pitch_classes = [pitchtools.NumberedPitchClass(float(x)) for x in pitches]
            object.__setattr__(self, '_pitches', tuple([float(x) for x in pitches]))
            object.__setattr__(self, '_pitch_classes', tuple([float(x) for x in pitch_classes]))
            return self.asset
        raise Exception('Asset does not exist for event %s' % self.event.name)

    def write(self, **kwargs):
        object.__setattr__(self, '_asset', self._find_chord())
        self.delete()
        output = open(self.path, 'wb')
        cPickle.dump(self.asset, output)
        output.close()
