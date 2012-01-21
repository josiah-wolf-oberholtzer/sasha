import numpy
import os
import struct
from sasha import SASHA
from sasha import SASHAROOT
from sasha.core.wrappers._Wrapper import _Wrapper


class FFTExtract(_Wrapper):

    ### PRIVATE METHODS ###

    def _execute(self,
        audio_filename,
        analysis_filename,
        feature_type,
        bands = 24,
        overwrite = True):

        assert os.path.exists(audio_filename)
        if os.path.exists(analysis_filename):
            if not overwrite:
                raise Exception('File exists: %s' % analysis_filename)
            else:
                os.remove(analysis_filename)

        if feature_type == 'chroma':
            assert bands in (12, 24)
            flags = '-c %d' % int(bands)
        elif feature_type == 'constant_q':
            assert 0 <= int(bands)
            flags = '-q %d' % int(bands)
        elif feature_type == 'log_harmonicity':
            flags = '-H'
        elif feature_type == 'log_power':
            flags = '-P'
        elif feature_type == 'mfcc':
            assert 0 < bands
            flags = '-m %d' % bands
        else:
            raise Exception('Unknown feature: "%s"' % feature_type)

        command = '%s -p %s -v 10 -C 2 -s %s %s %s %s' % \
            (self.executable,
            self.plan_path,
            100, # enforce common hop size
            flags,
            audio_filename,
            analysis_filename)

        out, err = self._exec(command)

    ### PUBLIC ATTRIBUTES ###

    @property
    def executable(self):
        return SASHA.get_binary('fftextract')

    @property
    def plan_path(self):
        return os.path.join(SASHAROOT, 'tmp', 'fftw_plan.txt')

    ### PUBLIC METHODS ###

    def delete_plan(self):
        if os.path.exists(self.plan_path):
            os.remove(self.plan_path)

    def read_analysis(self, analysis_filename):
        try:
            f = open(analysis_filename, 'r')
            q = f.read()
            f.close
        except:
            raise Exception('File not found: "%s"' % analysis_filename)

        vecsize = struct.unpack('i', q[:4])[0] # 4 chars in an int
        veccount = ((len(q) - 4) / vecsize) / 8 # 8 chars in a double

        analysis = numpy.zeros((veccount, vecsize), dtype = numpy.float)
        fmt = 'd' * vecsize

        for i in range(veccount):
            start = 4 + (i * vecsize * 8)
            stop = start + (vecsize * 8)
            vec = struct.unpack(fmt, q[start:stop])
            analysis[i] = vec

        return analysis

    def write_chroma(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'chroma', bands = 24)

    def write_constant_q(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'constant_q', bands = 24)

    def write_linear_spectrum(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'constant_q', bands = 0)

    def write_log_harmonicity(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'log_harmonicity')

    def write_log_power(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'log_power')

    def write_mfcc(self, audio_filename, analysis_filename):
        self._execute(audio_filename, analysis_filename, 'mfcc', bands = 24)

    def write_numpy(self, array, analysis_filename, overwrite = True):
        assert isinstance(array, numpy.ndarray)
        assert len(array.shape) == 2
        assert array.dtype == numpy.dtype('float64')
        
        if os.path.exists(analysis_filename):
            if not overwrite:
                raise Exception('File exists: %s' % analysis_filename)
            else:
                os.remove(analysis_filename)

        f = open(analysis_filename, 'w')
        f.write(struct.pack('i', array.shape[i])) # vector size
        for vector in array:
            f.write(struct.pack('d' * len(vector), *vector))
        f.close( )
