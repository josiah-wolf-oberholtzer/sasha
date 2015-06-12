import bisect
import numpy
from sasha.tools.analysistools.Peak import Peak
try:
    import pyfftw
    from pyfftw.interfaces.numpy_fft import rfft
    pyfftw.interfaces.cache.enable()
    print('Using pyfftw.')
except ImportError:
    from numpy.fft import rfft


class Frame(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_audio',
        '_frame_size',
        '_frequencies',
        '_frame_id',
        '_midis',
        '_offset',
        '_peaks',
        '_sampling_rate',
        )

    ### CONSTRUCTOR ###

    def __new__(
        cls,
        audio,
        frame_size,
        offset,
        sampling_rate,
        frame_id=None,
        ):
        self = object.__new__(cls)
        assert len(audio) <= frame_size
        self._audio = audio
        self._frame_size = frame_size
        self._frequencies = None
        self._frame_id = frame_id
        self._midis = None
        self._offset = offset
        self._peaks = None
        self._sampling_rate = sampling_rate
        return self

    ### SPECIAL METHODS ###

    def __call__(
        self,
        max_peak_count=None,
        max_peak_frequency=None,
        min_peak_frequency=None,
        ):
        # from sasha import sasha_configuration
        # sasha_configuration.logger.info('Calculating FFT @ %d' % self.offset)
        fft = rfft(self.windowed_audio)
        peaks = []
        mag = abs(fft)
        prev_mag = numpy.abs(mag[0])
        this_mag = numpy.abs(mag[1])
        next_mag = None
        for bin in range(2, len(mag) - 1):
            next_mag = numpy.abs(mag[bin])
            if (
                prev_mag < this_mag and
                next_mag < this_mag
                ):
                frequency = (bin - 1) * self.fundamental
                amplitude = this_mag
                phase = numpy.angle(fft[bin - 1])
                peak = Peak(
                    frequency,
                    amplitude,
                    phase,
                    frame_id=self.frame_id,
                    )
                peaks.append(peak)
            prev_mag = this_mag
            this_mag = next_mag
        self._peaks = self._filter_peaks(
            peaks,
            max_peak_count=max_peak_count,
            max_peak_frequency=max_peak_frequency,
            min_peak_frequency=min_peak_frequency,
            )
        self._frequencies = tuple(_.frequency for _ in self)
        self._midis = tuple(_.midis for _ in self)

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
            '_frame_id': self._frame_id,
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
        for key, value in state.items():
            setattr(self, key, value)

    ### PRIVATE METHODS ###

    def _filter_peaks(
        self,
        peaks,
        max_peak_frequency=None,
        min_peak_frequency=None,
        max_peak_count=None,
        ):
        if max_peak_frequency is not None:
            peaks = (_ for _ in peaks if _.frequency <= max_peak_frequency)
        if min_peak_frequency is not None:
            peaks = (_ for _ in peaks if min_peak_frequency <= _.frequency)
        if max_peak_count is not None:
            peaks = sorted(peaks, key=lambda x: x.amplitude, reverse=True)
            peaks = peaks[:max_peak_count]
            peaks.sort(key=lambda x: x.frequency)
        peaks = tuple(peaks)
        return peaks

    ### PUBLIC METHODS ###

    def find_peaks_within_midi_threshold_of_peak(self, peak, threshold):
        result = []
        idx = bisect.bisect(self.midis, peak.midis)

        if idx < len(self.peaks):  # ok to count up
            j = idx
            while j < len(self.peaks):
                if abs(self.peaks[j].midis - peak.midis) <= threshold:
                    result.append(self[j])
                    j += 1
                else:
                    break
        if 0 < idx:  # ok to count down
            j = idx - 1
            while 0 <= j:
                if abs(self.midis[j] - peak.midis) <= threshold:
                    result.append(self[j])
                    j -= 1
                else:
                    break
        result.sort(key=lambda x: abs(x.frequency - peak.frequency))
        return result

    ### PUBLIC PROPERTIES ###

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
    def frame_id(self):
        return self._frame_id

    @property
    def midis(self):
        return self._midis

    @property
    def offset(self):
        '''The offset in samples of this audio slice from the beginning of its
        source.
        '''
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