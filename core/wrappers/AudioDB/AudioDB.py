import os
from tempfile import NamedTemporaryFile

from sasha import SASHA
from sasha import SASHAROOT
from sasha.core.wrappers.Wrapper import Wrapper


class AudioDB(Wrapper):

    __slots__ = ('_klass', '_name', '_path')

    def __init__(self, name):
        path, klass = SASHA.get_audiodb_parameters(name)
        object.__setattr__(self, '_klass', klass)
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_path', path)

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.name))

    ### PUBLIC ATTRIBUTES ###

    @property
    def executable(self):
        return SASHA.get_binary('audiodb')

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def klass(self):
        return self._klass

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def status(self):
        out, err = self._exec('%s -d %s -S' % (self.executable, self.path))
        lines = filter(None, out.split('\n'))
        status = { }
        for line in lines:
            if line.startswith('num files'):
                status['num_files'] = int(line.partition(':')[-1])
            elif line.startswith('data dim'):
                status['data_dim'] = int(line.partition(':')[-1])
            elif line.startswith('total vectors'):
                status['total_vectors'] = int(line.partition(':')[-1].split()[0])
            elif line.startswith('vectors available'):
                status['available_vectors'] = int(line.partition(':')[-1].split()[0])
            elif line.startswith('total bytes'):
                status['total_bytes'] = int(line.partition(':')[-1].split()[0])
            elif line.startswith('bytes available'):
                status['available_bytes'] = int(line.partition(':')[-1].split()[0])
            elif line.startswith('flags'):
                flags = line.partition(':')[-1].split()
                for flag in flags:
                    name = flag.partition('[')[0]
                    value = flag.partition('[')[-1][:-1]
                    if value == 'on':
                        value = True
                    else:
                        value = False
                    status[name] = value
            elif line.startswith('null count'):
                status['null_count'] = int(line.split()[2])
                status['small_sequence_count'] = int(line.split()[-1])
        return status

    ### PUBLIC METHODS ###

    def create(self, overwrite = True):
        if self.exists:
            if overwrite:
                self.delete( )
            else:
                raise Exception('Database already exists.')
        
        out, err = self._exec('%s -N --datasize=100 -d %s' % (self.executable, self.path))
        out, err = self._exec('%s -L -d %s' % (self.executable, self.path))
        out, err = self._exec('%s -P -d %s' % (self.executable, self.path))

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def populate(self, events):
        from sasha.core.domain import Event
        from sasha.plugins.analysis import LogPowerAnalysis

        assert len(events) and all([isinstance(x, Event) for x in events])
        assert all([LogPowerAnalysis(x).exists for x in events])
        assert all([self.klass(x).exists for x in events])
        
        tmp_path = os.path.join(SASHAROOT, 'tmp')

        key_file_path = os.path.join(tmp_path, 'keys.txt')
        log_power_file_path = os.path.join(tmp_path, 'log_power.txt')
        feature_file_path = os.path.join(tmp_path, 'feature.txt')

        key_file = open(key_file_path, 'w')
        log_power_file = open(log_power_file_path, 'w')
        feature_file = open(feature_file_path, 'w')

        for event in events:
            key_file.write('%s\n' % event.name)
            log_power_file.write('%s\n' % LogPowerAnalysis(event).path)
            feature_file.write('%s\n' % self.klass(event).path)

        key_file.close( )
        log_power_file.close( )
        feature_file.close( )

        command = '%s -d %s -B -K %s -F %s -W %s -v 0' % \
            (self.executable, 
            self.path,
            key_file_path,
            feature_file_path,
            log_power_file_path)

        out, err = self._exec(command)


    def query(self, target, n = 10, events = [ ]):
        from sasha.core.domain import Event

        if not isinstance(target, Event):
            target = Event(target)
        assert 0 < n
        assert all([isinstance(x, Event) for x in events])

        feature = self.klass(target)

        command = '%s -d %s -Q sequence -e -n 1 -l 20 -R 0.5 -f %s' % \
            (self.executable, self.path, feature.path)

        if events:
            if target not in events:
                events.append(target)
            events = sorted(set(events))
            tempfile = NamedTemporaryFile(
                mode='w',
#                dir=os.path.join(SASHAROOT, 'tmp'),
                delete=False)
            for event in events:
                tempfile.write('%s\n' % event.name)
            tempfile.close( )
            command += ' -r %d -K %s' % (len(events), tempfile.name)
            out, err = self._exec(command)
            os.unlink(tempfile.name)
        else:
            command += ' -r %d' % (n + 1)
            out, err = self._exec(command)

        q = filter(None, [x.split( ) for x in out.split('\n')])

        results = [ ]
        for x in q:
            distance = float(x[1])
            name = os.path.basename(x[0])
            event = Event.get(name=name)[0]
            if event.name != target.name:
                results.append((distance, event))

        return tuple(results[:n])
