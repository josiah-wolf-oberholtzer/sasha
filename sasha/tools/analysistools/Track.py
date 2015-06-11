import math
from sasha.tools.analysistools.Peak import Peak


class Track(object):

    __slots__ = (
        '_peaks',
        )

    ### INITIALIZER ###

    def __init__(self, peaks):
        self._peaks = tuple(peaks)

    ### OVERRIDES ###

    def __eq__(self, other):
        if type(self) == type(other):
            if self.peaks == other.peaks:
                return True
        return False

    def __getitem__(self, item):
        return self._peaks[item]

    def __getstate__(self):
        state = {
            '_peaks': self.peaks
            }
        return state

    def __iter__(self):
        for peak in self._peaks:
            yield peak

    def __len__(self):
        return len(self._peaks)

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### PUBLIC ATTRIBUTES ###

    @property
    def amplitude_mean(self):
        return sum([p.amplitude for p in self]) / len(self)

    @property
    def cents_deviation_centroid(self):
        return 100 * (self.midis_centroid - self.semitones_centroid)

    @property
    def frequency_centroid(self):
        return sum([p.frequency * p.amplitude for p in self]) / \
            sum([p.amplitude for p in self])

    @property
    def frequency_mean(self):
        return sum([p.frequency for p in self]) / len(self)

    @property
    def midis_centroid(self):
        return sum([p.midis * p.amplitude for p in self]) / \
            sum([p.amplitude for p in self])

    @property
    def midis_mean(self):
        return sum([p.midis for p in self]) / len(self)

    @property
    def semitones_centroid(self):
        return round(self.midis_centroid * 2.) / 2.

    @property
    def peaks(self):
        return self._peaks

    @property
    def start_frame(self):
        return self[0].frame_ID

    @property
    def stop_frame(self):
        return self[-1].frame_ID

    ### PUBLIC METHODS ###

    def db(self, reference):
        if isinstance(reference, Track):
            reference = reference.amplitude_mean
        elif isinstance(reference, Peak):
            reference = reference.amplitude
        return 10. * math.log(self.amplitude_mean / reference, 10.)