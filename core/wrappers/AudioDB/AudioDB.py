import os
from tempfile import NamedTemporaryFile

from sasha import SASHACFG
from sasha import SASHAROOT
from sasha.core.wrappers._Wrapper import _Wrapper


class AudioDB(_Wrapper):

    __slots__ = ('_klass', '_name', '_path')

    def __init__(self, name):
        path, klass = SASHACFG.get_audiodb_parameters(name)
        object.__setattr__(self, '_klass', klass)
        object.__setattr__(self, '_name', name)
        object.__setattr__(self, '_path', path)

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.name))

    ### PUBLIC ATTRIBUTES ###

    @property
    def executable(self):
        return SASHACFG.get_binary('audiodb')

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
        print out

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

        command = '%s -d %s -Q sequence -e -l 20 -R 2.0 -f %s' % \
            (self.executable, self.path, feature.path)

        if events:
            if target not in events:
                events.append(target)
            events = sorted(set(events))
            tempfile = NamedTemporaryFile(
                mode='w',
                dir=os.path.join(SASHAROOT, 'tmp'),
                delete=False)
            for event in events:
                tempfile.write('%s\n' % event.name)
            tempfile.close( )
            command += ' -n %d -K %s' % (len(events), tempfile.name)
            out, err = self._exec(command)
        else:
            command += ' -n %d' % (n + 1)
            out, err = self._exec(command)

        q = filter(None, [x.split( ) for x in out.split('\n')])

        results = [ ]
        for x in q[1:n+1]:
            distance = int(x[1])
            name = os.path.basename(x[0])
            event = Event.get(name=name)[0]
            results.append((distance, event))

        return tuple(results)
