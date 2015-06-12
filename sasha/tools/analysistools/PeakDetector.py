import multiprocessing
import numpy
from sasha.tools.analysistools.Frame import Frame
from sasha.tools.analysistools.PeakDetectionWorker import PeakDetectionWorker


class PeakDetector(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_frame_size',
        '_hop_size',
        '_max_peak_count',
        '_max_peak_frequency',
        '_min_peak_frequency',
        '_window_size',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        max_peak_count=60,
        max_peak_frequency=4000,
        min_peak_frequency=100,
        ):
        self._frame_size = 16384
        self._hop_size = 256
        self._max_peak_count = int(max_peak_count)
        self._max_peak_frequency = float(max_peak_frequency)
        self._min_peak_frequency = float(min_peak_frequency)
        self._window_size = 2048

    ### SPECIAL METHODS ###

    def __call__(self, audio, parallel=True):
        from sasha.tools.assettools import SourceAudio
        if not isinstance(audio, SourceAudio):
            audio = SourceAudio(audio)
        assert audio.exists
        tasks = self._create_tasks(audio)
        frames = []
        if parallel:
            task_queue = multiprocessing.JoinableQueue()
            result_queue = multiprocessing.Queue()
            workers = [
                PeakDetectionWorker(
                    task_queue,
                    result_queue,
                    max_peak_count=self.max_peak_count,
                    max_peak_frequency=self.max_peak_frequency,
                    min_peak_frequency=self.min_peak_frequency,
                    )
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
                task(
                    max_peak_count=self.max_peak_count,
                    max_peak_frequency=self.max_peak_frequency,
                    min_peak_frequency=self.min_peak_frequency,
                    )
                frames.append(task)
        assert all(isinstance(x, Frame) for x in frames)
        frames.sort(key=lambda x: x.offset)
        return frames

    ### PRIVATE METHODS ###

    def _create_tasks(self, audio):
        samples, sampling_rate = audio.read()
        frames = []
        offset = 0
        frame_id = 0
        while offset < len(samples):
            frame = Frame(
                samples[offset:offset + self.window_size],
                self.frame_size,
                offset,
                sampling_rate,
                frame_id=frame_id,
                )
            frames.append(frame)
            offset += self.hop_size
            frame_id += 1
        return frames

    ### PUBLIC METHODS ###

    def plot(self, frames):
        import matplotlib.pyplot as plt
        from matplotlib import cm
        # from matplotlib import rc
        # rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
        fig = plt.figure()
        ax = fig.add_subplot(111)
        peaks = []
        for frame in frames:
            for peak in frame:
                peaks.append(peak)
        peaks.sort(key=lambda x: x.amplitude)
        frame_ids = [peak.frame_id for peak in peaks]
        midis = [peak.midis for peak in peaks]
        max_amp = max(peak.amplitude for peak in peaks)
        dbs = numpy.array(peak.db(max_amp) for peak in peaks)
        dbs -= dbs.min()
        dbs /= dbs.max()
        ax.scatter(frame_ids, midis,
            alpha=0.5,
            c=dbs,
            cmap=cm.Greys,
            edgecolors='none',
            marker='o',
            s=10 * (dbs ** 2.),
            )
        return fig

    ### PUBLIC PROPERTIES ###

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