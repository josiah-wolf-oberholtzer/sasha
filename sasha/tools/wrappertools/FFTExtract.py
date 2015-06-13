import numpy
import os
import struct
from sasha.tools.wrappertools.Wrapper import Wrapper


class FFTExtract(Wrapper):

    ### INITIALIZER ###

    def __init__(self):
        import os
        from sasha.tools.wrappertools import Which
        if not os.path.isabs(self.executable):
            assert Which()('fftExtract') is not None

    ### PRIVATE METHODS ###

    def _execute(
        self,
        audio_filename,
        analysis_filename,
        feature_type,
        bands=24,
        overwrite=True,
        ):
        assert os.path.exists(audio_filename)
        analysis_directory, _ = os.path.split(analysis_filename)
        if not os.path.exists(analysis_directory):
            os.makedirs(analysis_directory)
        if os.path.exists(analysis_filename):
            if not overwrite:
                raise Exception('File exists: {}'.format(analysis_filename))
            else:
                os.remove(analysis_filename)
        if feature_type == 'chroma':
            assert bands in (12, 24)
            flags = '-c {}'.format(bands)
        elif feature_type == 'constant_q':
            assert 0 <= int(bands)
            flags = '-q {}'.format(bands)
        elif feature_type == 'log_harmonicity':
            flags = '-H'
        elif feature_type == 'log_power':
            flags = '-P'
        elif feature_type == 'mfcc':
            assert 0 < bands
            flags = '-m {} -M 3 -g 0'.format(bands)
        else:
            raise Exception('Unknown feature: {!r}'.format(feature_type))
        command = '{} -p {} -v 10 -C 2 -s {} {} {} {}'.format(
            self.executable,
            self.plan_path,
            100,  # enforce common hop size
            flags,
            audio_filename,
            analysis_filename,
            )
        print(command)
        out, err = self._exec(command)
        if err:
            print err

    ### PUBLIC METHODS ###

    def delete_plan(self):
        if os.path.exists(self.plan_path):
            os.remove(self.plan_path)

    def read_analysis(self, analysis_filename):
        with open(analysis_filename, 'r') as file_pointer:
            binary_contents = file_pointer.read()
        number_size = 8
        vector_size = struct.unpack('i', binary_contents[:4])[0]
        vector_count = ((len(binary_contents) - 4) / vector_size) / number_size
        analysis = numpy.zeros((vector_count, vector_size), dtype=numpy.float)
        format_string = 'd' * vector_size
        for i in range(vector_count):
            start = 4 + (i * vector_size * number_size)
            stop = start + (vector_size * number_size)
            vector = struct.unpack(format_string, binary_contents[start:stop])
            analysis[i] = vector
        return analysis

    def write_chroma(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'chroma', bands=24)

    def write_constant_q(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'constant_q', bands=24)

    def write_linear_spectrum(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'constant_q', bands=0)

    def write_log_harmonicity(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'log_harmonicity')

    def write_log_power(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'log_power')

    def write_mfcc(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'mfcc', bands=24)

    def write_numpy(self, array, analysis_filename, overwrite=True):
        assert isinstance(array, numpy.ndarray)
        assert len(array.shape) == 2
        assert array.dtype == numpy.dtype('float64')
        if os.path.exists(analysis_filename):
            if not overwrite:
                raise Exception('File exists: {}'.format(analysis_filename))
            else:
                os.remove(analysis_filename)
        with open(analysis_filename, 'w') as file_pointer:
            bytestring = struct.pack('i', array.shape[1])
            file_pointer.write(bytestring)  # vector size
            for vector in array:
                bytestring = struct.pack('d' * len(vector), *vector)
                file_pointer.write(bytestring)

    ### PUBLIC PROPERTIES ###

    @property
    def executable(self):
        from sasha import sasha_configuration
        return sasha_configuration.get_binary('fftextract')

    @property
    def plan_path(self):
        import sasha
        sasha_root = sasha.__path__[0]
        return os.path.join(sasha_root, 'tmp', 'fftw_plan.txt')