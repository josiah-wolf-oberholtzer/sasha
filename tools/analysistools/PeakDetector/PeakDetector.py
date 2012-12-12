import multiprocessing
import numpy
from sasha.tools.analysistools.Frame import Frame
from sasha.tools.analysistools.PeakDetectionWorker import PeakDetectionWorker


class PeakDetector(object):

    __slots__ = ('_frame_size', '_hop_size', '_max_peak_count',
        '_max_peak_frequency', '_min_peak_frequency', '_window_size')

    def __init__(self, **kwargs):
        self._frame_size = 16384
        self._hop_size = 256
        self._max_peak_count = 60
        self._max_peak_frequency = 4000
        self._min_peak_frequency = 100
        self._window_size = 2048
        for k, v in kwargs.iteritems():
            if hasattr(self, k):
                setattr(self, k, v)

    ### OVERRIDES ###

    def __call__(self, audio, parallel = True):
        from sasha.plugins import SourceAudio

        if not isinstance(audio, SourceAudio):
            audio = SourceAudio(audio)
        assert audio.exists

        kwargs = self._get_kwargs()
        tasks = self._create_tasks(audio)
        frames = [ ]

        if parallel:

            task_queue = multiprocessing.JoinableQueue()
            result_queue = multiprocessing.Queue()
            workers = [PeakDetectionWorker(task_queue, result_queue, **kwargs)
                for i in range(multiprocessing.cpu_count() * 2)]
            for worker in workers:
                worker.start()
            for task in tasks:
                task_queue.put(task)
            for i in xrange(len(tasks)):
                frames.append(result_queue.get())
            for worker in workers:
                task_queue.put(None)
            task_queue.join()
            result_queue.close()
            task_queue.close()
            for worker in workers:
                worker.join()

        else:

            for task in tasks:
                task(**kwargs)
                frames.append(task)

        assert all([isinstance(x, Frame) for x in frames])

        frames.sort(key = lambda x: x.offset)

        return frames

    ### PRIVATE METHODS ###

    def _create_tasks(self, audio):
        samples, sampling_rate = audio.read()
        frames = [ ]
        offset = 0
        ID = 0
        while offset < len(samples):
            frames.append(Frame(
                samples[offset:offset + self.window_size],
                self.frame_size,
                offset,
                sampling_rate,
                ID = ID))
            offset += self.hop_size
            ID += 1
        return frames

    def _get_kwargs(self):
        kwargs = { }
        for k in [
            'max_peak_count',
            'max_peak_frequency',
            'min_peak_frequency']:
            kwargs[k] = getattr(self, k)
        return kwargs

    ### PUBLIC ATTRIBUTES ###

    @property
    def frame_size(self):
        return self._frame_size

    @frame_size.setter
    def frame_size(self, arg):
        if 0 < arg:
            self._frame_size = int(arg)

    @property
    def hop_size(self):
        return self._hop_size

    @hop_size.setter
    def hop_size(self, arg):
        if 0 < arg:
            self._hop_size = int(arg)

    @property
    def max_peak_count(self):
        return self._max_peak_count

    @max_peak_count.setter
    def max_peak_count(self, arg):
        if 0 < arg:
            self._max_peak_count = int(arg)

    @property
    def max_peak_frequency(self):
        return self._max_peak_frequency

    @max_peak_frequency.setter
    def max_peak_frequency(self, arg):
        if 0 < arg:
            self._max_peak_frequency = float(arg)

    @property
    def min_peak_frequency(self):
        return self._min_peak_frequency

    @min_peak_frequency.setter
    def min_peak_frequency(self, arg):
        if 0 <= arg:
            self._min_peak_frequency = float(arg)

    @property
    def window_size(self):
        return self._window_size

    @window_size.setter
    def window_size(self, arg):
        if 0 < arg:
            self._window_size = int(arg)

    ### PUBLIC METHODS ###

    def plot(self, frames):
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from matplotlib import rc

#        rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})

        fig = plt.figure()
        ax = fig.add_subplot(111)

        peaks = [ ]
        for frame in frames:
            for peak in frame:
                peaks.append(peak)

        peaks.sort(key = lambda x: x.amplitude)

        frame_ids = [peak.frame_ID for peak in peaks]
        midis = [peak.midis for peak in peaks]
        max_amp = max([peak.amplitude for peak in peaks])
        dbs = numpy.array([peak.db(max_amp) for peak in peaks])
        dbs -= dbs.min()
        dbs /= dbs.max()

        ax.scatter(frame_ids, midis,
            alpha = 0.5,
            c = dbs,
            cmap = cm.Greys,
            edgecolors = 'none',
            marker = 'o', 
            s = 10 * (dbs ** 2.),
            )

        return fig
