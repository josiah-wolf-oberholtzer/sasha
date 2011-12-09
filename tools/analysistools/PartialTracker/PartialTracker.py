import numpy
from bisect import bisect
from sasha.tools.analysistools.Peak import Peak
from sasha.tools.analysistools.Regression import Regression
from sasha.tools.analysistools.Track import Track


class PartialTracker(object):

    __slots__ = (
        '_max_deviation_in_midis',
        '_max_partial_gap',
        '_min_track_length',
        '_peak_sort',
        '_regression_size',
        '_use_regression',
    )

    def __init__(self, **kwargs):
        self.max_deviation_in_midis = 0.15
        self.max_partial_gap = 1
        self.min_track_length = 10
        self.peak_sort = 'strongest'
        self.use_regression = True
        self.regression_size = 8
        for k, v in kwargs.iteritems( ):
            if hasattr(self, k):
                setattr(self, k, v)

    ### OVERRIDES ###

    def __call__(self, frames):

        regression = Regression( )

        # find links between peaks
        for i in xrange(len(frames) - 2):

            peaks = self._sort_peaks_in_frame(frames[i])
            for peak in filter(lambda x: x.next_peak is None, peaks):

                prediction = peak.midis
                can_predict = False
                if self.use_regression:
                    chain = self._build_peak_chain_backwards(peak)
                    if len(chain) == self.regression_size:
                        xs = numpy.array([x.frame_ID for x in chain]).reshape(-1, 1)
                        ys = numpy.array([x.midis for x in chain])
                        regression.learn(xs, ys)
                        can_predict = True

                frame_ids = range(i + 1, i + 2 + self.max_partial_gap)
                for j in filter(lambda x: x < len(frames), frame_ids):
                    frame = frames[j]

                    if self.use_regression and can_predict:
                        prediction = regression.predict(numpy.array([[j]]))[0]

                    candidates = self._find_peaks_in_frame_within_midi_threshold_of_midis(
                        prediction, frame, self.max_deviation_in_midis)

                    if candidates:
                        # we're too close to another track
                        if any([x.previous_peak is not None for x in candidates]):
                            break
                        # we're not too close, so free to link
                        self._link_peaks(peak, candidates[0])
                        break

                    # try opposite slope of regression prediction
                    if self.use_regression and can_predict:
                        prediction = peak.midis + (peak.midis - prediction)

                        candidates = self._find_peaks_in_frame_within_midi_threshold_of_midis(
                            prediction, frame, self.max_deviation_in_midis)

                        if candidates:
                            # we're too close to another track
                            if any([x.previous_peak is not None for x in candidates]):
                                break
                            # we're not too close, so free to link
                            self._link_peaks(peak, candidates[0])
                            break

        tracks = self._create_tracks_from_analyzed_frames(frames)

        return tuple(filter(lambda x: self.min_track_length <= len(x), tracks))

    ### PRIVATE METHODS ###

    def _build_peak_chain_backwards(self, peak):
        chain = [peak]
        while chain[-1].previous_peak is not None:
            chain.append(chain[-1].previous_peak)
            if len(chain) == self.regression_size:
                break
        return tuple(reversed(chain))

    def _find_peaks_in_frame_within_midi_threshold_of_midis(self, midis, frame, threshold):
        result = [ ]
        frame_midis = [x.midis for x in frame]
        idx = bisect(frame_midis, midis)
        
        if idx < len(frame): # ok to count up
            j = idx
            while j < len(frame):
                if abs(frame_midis[j] - midis) <= threshold:
                    result.append(frame[j])
                    j += 1
                else:
                    break
    
        if 0 < idx: # ok to count down
            j = idx - 1
            while 0 <= j:
                if abs(frame_midis[j] - midis) <= threshold:
                    result.append(frame[j])
                    j -= 1
                else:
                    break
    
        result.sort(key = lambda x: abs(x.midis - midis))
        return result

    def _create_tracks_from_analyzed_frames(self, frames):
        track_starts = [ ]
        for frame in frames:
            for peak in frame:
                if peak.previous_peak is None and \
                    peak.next_peak is not None:
                    track_starts.append(peak)
                elif peak.is_free_peak:
                    track_starts.append(peak)

        tracks = [ ]
        for track_start in track_starts:
            track = [track_start]
            this = track_start
            while this.next_peak is not None:
                this = this.next_peak
                track.append(this)
            tracks.append(Track(track))

        return tracks


    def _link_peaks(self, a, b):
        if a.frame_ID < b.frame_ID:
            a.next_peak = b
            b.previous_peak = a
        elif b.frame_ID < a.frame_ID:
            b.next_peak = a
            a.previous_peak = b
        else:
            raise Exception("Can't link peaks in the same frame.")

    def _sort_peaks_in_frame(self, frame):
        if self.peak_sort == 'strongest':
            return tuple(sorted(frame, key = lambda x: x.amplitude, reverse = True))
        elif self.peak_sort == 'lowest':
            return tuple(sorted(frame, key = lambda x: x.frequency))
        else:
            raise Exception('Unknown peak sort.')

    ### PUBLIC ATTRIBUTES ###

    @property
    def max_deviation_in_midis(self):
        return self._max_deviation_in_midis

    @max_deviation_in_midis.setter
    def max_deviation_in_midis(self, arg):
        if not 0 <= arg:
            raise ValueError
        self._max_deviation_in_midis = float(arg)

    @property
    def max_partial_gap(self):
        return self._max_partial_gap

    @max_partial_gap.setter
    def max_partial_gap(self, arg):
        if not 0 <= arg:
            raise ValueError
        self._max_partial_gap = int(arg)

#    @property
#    def max_partials_per_frame(self):
#        return self._max_partials_per_frame

#    @max_partials_per_frame.setter
#    def max_partials_per_frame(self, arg):
#        if not 1 <= arg:
#            raise ValueError
#        self._max_partials_per_frame = int(arg)

    @property
    def min_track_length(self):
        return self._min_track_length

    @min_track_length.setter
    def min_track_length(self, arg):
        if not 1 <= arg:
            raise ValueError
        self._min_track_length = int(arg)

    @property
    def peak_sort(self):
        return self._peak_sort

    @peak_sort.setter
    def peak_sort(self, arg):
        if not arg in ['strongest', 'lowest']:
            raise ValueError
        self._peak_sort = arg

    @property
    def regression_size(self):
        return self._regression_size

    @regression_size.setter
    def regression_size(self, arg):
        if arg < 2:
            raise ValueError
        self._regression_size = int(arg)

    @property
    def use_regression(self):
        return self._use_regression

    @use_regression.setter
    def use_regression(self, arg):
        if not arg in [True, False]:
            raise ValueError
        self._use_regression = arg

    ### PUBLIC METHODS ###

    def plot(self, tracks, mode = 0, minimum_track_size = 10):

        import matplotlib.pyplot as plt
        from matplotlib import cm
        from matplotlib.collections import LineCollection
        from matplotlib.colors import LogNorm, Normalize
        from matplotlib import cm
        from matplotlib import rc

#        rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

        assert mode in [0, 1]

        minimum_track_size = max(2, minimum_track_size)

        fig = plt.figure( )

        if mode == 0:

            z_min = z_max = None
            for track in filter(lambda x: minimum_track_size <= len(x), tracks):
                if z_min is None:
                    z_min = min([peak.amplitude for peak in track])
                else:
                    z_min = min(z_min, min([peak.amplitude for peak in track]))
                if z_max is None:
                    z_max = max([peak.amplitude for peak in track])
                else:
                    z_max = max(z_max, max([peak.amplitude for peak in track]))

            cmap = cm.gray
            norm = LogNorm(vmin = z_min, vmax = z_max)

            x_min = x_max = y_min = y_max = None
            for track in filter(lambda x: minimum_track_size <= len(x), tracks):
                xs = numpy.array([peak.frame_ID for peak in track])
                ys = numpy.array([peak.midis for peak in track])
                zs = numpy.array([peak.amplitude for peak in track])

                if x_min is None:
                    x_min = xs.min( )
                else:
                    x_min = min(x_min, xs.min( ))

                if x_max is None:
                    x_max = xs.max( )
                else:
                    x_max = max(x_max, xs.max( ))

                if y_min is None:
                    y_min = ys.min( )
                else:
                    y_min = min(y_min, ys.min( ))

                if y_max is None:
                    y_max = ys.max( )
                else:
                    y_max = max(y_max, ys.max( ))

                points = numpy.array([xs, ys]).T.reshape(-1, 1, 2)
                segments = numpy.concatenate([points[:-1], points[1:]], axis=1)

                lc = LineCollection(segments, cmap=cmap, norm=norm)
                lc.set_array(zs)
                lc.set_linewidth(1)

                fig.gca( ).add_collection(lc)                
                fig.gca( ).set_xlim(x_min, x_max)
                fig.gca( ).set_ylim(y_min, y_max)

        elif mode == 1:

            for track in filter(lambda x: minimum_track_size <= len(x), tracks):
                xs = [peak.frame_ID for peak in track]
                ys = [peak.midis for peak in track]
                fig.gca( ).plot(xs, ys)

        ax = fig.gca( )            
        ax.set_xlabel('Frames')
        ax.set_ylabel('Semitones (0 = Middle C)')
        ax.set_axis_bgcolor('black')

        return fig
