from bisect import *

import numpy

from sasha.tools.systemtools import Immutable
from sasha.tools.analysistools.Peak import Peak

try:
    from anfft import rfft
except ImportError:
    from numpy.fft import rfft


class Frame(Immutable):

    __slots__ = (
        '_audio',
        '_frame_size',
        '_frequencies',
        '_ID',
        '_midis',
        '_offset',
        '_peaks',
        '_sampling_rate',
        )

    def __new__(klass, audio, frame_size, offset, sampling_rate, ID = None):
        self = object.__new__(klass)
        assert len(audio) <= frame_size
        object.__setattr__(self, '_audio', audio)
        object.__setattr__(self, '_frame_size', frame_size)
        object.__setattr__(self, '_frequencies', None)
        object.__setattr__(self, '_ID', ID)
        object.__setattr__(self, '_midis', None)
        object.__setattr__(self, '_offset', offset)
        object.__setattr__(self, '_peaks', None)
        object.__setattr__(self, '_sampling_rate', sampling_rate)
        return self

    ### OVERRIDES ###

    def __call__(self, **kwargs):
        from sasha import sasha_configuration
        #sasha_configuration.logger.info('Calculating FFT @ %d' % self.offset)

        fft = rfft(self.windowed_audio)

        peaks = []
        mag = abs(fft)
        prev_mag = numpy.abs(mag[0])
        this_mag = numpy.abs(mag[1])
        next_mag = None

        for bin in range(2, len(mag) - 1):
            next_mag = numpy.abs(mag[bin])
            if (prev_mag < this_mag) and (next_mag < this_mag):
                frequency = (bin - 1) * self.fundamental
                amplitude = this_mag
                phase = numpy.angle(fft[bin - 1])
                peaks.append(Peak(frequency, amplitude, phase, frame_ID = self.ID))
            prev_mag = this_mag
            this_mag = next_mag

        object.__setattr__(self, '_peaks', self._filter_peaks(peaks, **kwargs))
        object.__setattr__(self, '_frequencies', [peak.frequency for peak in self])
        object.__setattr__(self, '_midis', [peak.midis for peak in self])

    def __eq__(self, other):
        if type(self) == type(other) and \
            self.audio == other.audio and \
            self.frame_size == other.frame_size and \
            self.offset == other.offset and \
            self.peaks == other.peaks and \
            self.sampling_rate == other.sampling_rate:
            return True
        return False

    def __getitem__(self, item):
        if self.peaks:
            return self.peaks[item]
        return None

    def __getnewargs__(self):
        return self.audio, self.frame_size, self.offset, self.sampling_rate

    def __getstate__(self):
        state = {
            '_audio': self._audio,
            '_frame_size': self._frame_size,
            '_frequencies': self._frequencies,
            '_ID': self._ID,
            '_midis': self._midis,
            '_offset': self._offset,
            '_peaks': self._peaks,
            '_sampling_rate': self._sampling_rate
        }
        return state

    def __iter__(self):
        if self.peaks:
            for peak in self.peaks:
                yield peak
        return

    def __len__(self):
        return len(self.peaks)

    def __setstate__(self, state):
        for k, v in state.iteritems():
            object.__setattr__(self, k, v)

    ### PRIVATE METHODS ###

    def _filter_peaks(self, peaks, **kwargs):
        if 'max_peak_frequency' in kwargs:
            peaks = filter(lambda x: x.frequency <= kwargs['max_peak_frequency'], peaks)
        if 'min_peak_frequency' in kwargs:
            peaks = filter(lambda x: kwargs['min_peak_frequency'] <= x.frequency, peaks)
        if 'max_peak_count' in kwargs:
            peaks.sort(key = lambda x: x.amplitude, reverse = True)
            peaks = peaks[:kwargs['max_peak_count']]
            peaks.sort(key = lambda x: x.frequency)
        return peaks

    ### PUBLIC ATTRIBUTES ###

    @property
    def audio(self):
        '''The audio slice to be analyzed.'''
        return self._audio

    @property
    def frequencies(self):
        return self._frequencies

    @property
    def frame_size(self):
        '''The size of the spectral frame.'''
        return self._frame_size

    @property
    def fundamental(self):
        '''The fundamental frequency.'''
        return float(self.sampling_rate) / self.frame_size

    @property
    def ID(self):
        return self._ID

    @property
    def midis(self):
        return self._midis

    @property
    def offset(self):
        '''The offset in samples of this audio slice from the beginning of its source.'''
        return self._offset

    @property
    def peaks(self):
        '''A tuple of spectral peaks.'''
        return self._peaks

    @property
    def sampling_rate(self):
        '''The sampling rate of the audio to be analyzed.'''
        return self._sampling_rate

    @property
    def window(self):
        '''The spectral window.'''
        window = numpy.hstack([
            numpy.hamming(len(self.audio)),
            numpy.zeros(self.frame_size - len(self.audio))
            ])
        return window / sum(window)

    @property
    def windowed_audio(self):
        '''The windowed audio.'''
        return numpy.hstack([
            self.audio,
            numpy.zeros(self.frame_size - len(self.audio))
            ]) * self.window

    ### PUBLIC METHODS ###

    def find_peaks_within_midi_threshold_of_peak(self, peak, threshold):
        result = []
        idx = bisect(self.midis, peak.midis)

        if idx < len(self.peaks): # ok to count up
            j = idx
            while j < len(self.peaks):
                if abs(self.peaks[j].midis - peak.midis) <= threshold:
                    result.append(self[j])
                    j += 1
                else:
                    break

        if 0 < idx: # ok to count down
            j = idx - 1
            while 0 <= j:
                if abs(self.midis[j] - peak.midis) <= threshold:
                    result.append(self[j])
                    j -= 1
                else:
                    break

        result.sort(key = lambda x: abs(x.frequency - peak.frequency))
        return result