import math


class Peak(object):

    # TODO: make it mutable again

    __slots__ = ('_amplitude', '_frame_ID', '_frequency', '_next_peak', '_phase', '_previous_peak',)

    def __init__(self, frequency, amplitude, phase, frame_ID = None):
        self._amplitude = amplitude
        self._frame_ID = frame_ID
        self._frequency = frequency
        self._next_peak = None
        self._phase = phase
        self._previous_peak = None
    
    ### OVERRIDES ###

    def __getnewargs__(self):
        return self.frequency, self.amplitude, self.phase

    def __getstate__(self):
        state = {
            '_amplitude': self._amplitude,
            '_frame_ID': self._frame_ID,
            '_frequency': self._frequency,
            '_phase': self._phase,
        }
        return state

    def __repr__(self):
        return '%s(%s, %s, %s)' % (self.__class__.__name__,
            self.frequency, self.amplitude, self.phase)

    def __setstate__(self, state):
        for k, v in state.iteritems( ):
            object.__setattr__(self, k, v)
        object.__setattr__(self, '_next_peak', None)
        object.__setattr__(self, '_previous_peak', None)

    ### PUBLIC ATTRIBUTES ###

    @property
    def amplitude(self):
        return self._amplitude

    @property
    def cents_deviation(self):
        return (self.midis - self.semitones) * 100

    @property
    def frame_ID(self):
        return self._frame_ID

    @property
    def frequency(self):
        return self._frequency

    @property
    def midis(self):
        return 9 + 12 * math.log(self.frequency / 440.) / math.log(2)

    @property
    def phase(self):
        return self._phase

    @property
    def semitones(self):
        return round(self.midis * 2.) / 2.

    ### PARTIAL TRAVERSAL ATTRIBUTES ###

    @property
    def is_end_of_partial(self):
        if self.next_peak is self:
            return True
        return False

    @property
    def is_free_peak(self):
        if self.previous_peak is None and \
            self.next_peak is None:
            return True
        return False

    @property
    def is_start_of_partial(self):
        if self.previous_peak is self:
            return True
        return False

    @property
    def is_orphaned_partial(self):
        if self.previous_peak is self and \
            self.next_peak is self:
            return True
        return False

    @property
    def is_unbegun_partial(self):
        if self.previous_peak is None:
            return True
        return False

    @property
    def is_unended_partial(self):
        if self.next_peak is None:
            return True
        return False

    @property
    def next_peak(self):
        return self._next_peak

    @next_peak.setter
    def next_peak(self, arg):
        assert isinstance(arg, (type(None), type(self)))
        self._next_peak = arg

    @property
    def previous_peak(self):
        return self._previous_peak

    @previous_peak.setter
    def previous_peak(self, arg):
        assert isinstance(arg, (type(None), type(self)))
        self._previous_peak = arg

    ### PUBLIC METHODS ###

    def db(self, reference):
        return 10. * math.log(self.amplitude / float(reference), 10.)


