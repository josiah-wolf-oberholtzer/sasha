import os
import shutil
import tempfile

from sasha.tools.executabletools.Executable import Executable


class AudioDB(Executable):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_asset_class',
        '_name',
        '_path',
        )

    ### INITIALIZER ###

    def __init__(self, name):
        from sasha import sasha_configuration
        import os
        if not os.path.isabs(self.executable):
            assert Executable.find_executable('audioDB') is not None
        path, asset_class = sasha_configuration.get_audiodb_parameters(name)
        self._asset_class = asset_class
        self._name = name
        self._path = path

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '{}({})'.format(self.__class__.__name__, repr(self.name))

    ### PUBLIC METHODS ###

    def create(self, overwrite=True):
        if self.exists:
            if overwrite:
                self.delete()
            else:
                raise Exception('Database already exists.')
        command = '{} -N --datasize=100 -d {}'
        command = command.format(self.executable, self.path)
        out, err = self._exec(command)
        command = '{} -L -d {}'.format(self.executable, self.path)
        out, err = self._exec(command)
        command = '{} -P -d {}'.format(self.executable, self.path)
        out, err = self._exec(command)

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def populate(self, events):
        from sasha.tools.domaintools import Event
        from sasha.tools.assettools import LogPowerAnalysis
        assert len(events) and all(isinstance(x, Event) for x in events)
        assert all(LogPowerAnalysis(x).exists for x in events)
        assert all(self.asset_class(x).exists for x in events)
        temporary_directory_path = tempfile.mkdtemp()
        key_file_path = os.path.join(
            temporary_directory_path,
            'keys.txt',
            )
        with open(key_file_path, 'w') as file_pointer:
            for event in events:
                string = '{}\n'.format(event.name)
                file_pointer.write(string)
        log_power_file_path = os.path.join(
            temporary_directory_path,
            'log_power.txt',
            )
        with open(log_power_file_path, 'w') as file_pointer:
            for event in events:
                string = '{}\n'.format(LogPowerAnalysis(event).path)
                file_pointer.write(string)
        feature_file_path = os.path.join(
            temporary_directory_path,
            'feature.txt',
            )
        with open(feature_file_path, 'w') as file_pointer:
            for event in events:
                string = '{}\n'.format(self.asset_class(event).path)
                file_pointer.write(string)
        command = '{} -d {} -B -K {} -F {} -W {} -v 0'.format(
            self.executable,
            self.path,
            key_file_path,
            feature_file_path,
            log_power_file_path,
            )
        stdout, stderr = self._exec(command)
        shutil.rmtree(temporary_directory_path)

    def query(self, target, n=10, events=None):
        from sasha.tools.domaintools import Event
        if not events:
            events = []
        if not isinstance(target, Event):
            target = Event(target)
        assert 0 < n
        assert all([isinstance(x, Event) for x in events])
        feature = self.asset_class(target)
        command = '{} -d {} -Q sequence -e -n 1 -l 20 -R 0.5 -f {}'.format(
            self.executable,
            self.path,
            feature.path,
            )
        print(command)
        if events:
            if target not in events:
                events.append(target)
            events = sorted(set(events))
            temporary_file = tempfile.NamedTemporaryFile(
                mode='w',
                # dir=os.path.join(sasha_root, 'tmp'),
                delete=False,
                )
            for event in events:
                temporary_file.write('{}\n'.format(event.name))
            temporary_file.close()
            command += ' -r {} -K {}'.format(len(events), temporary_file.name)
            out, err = self._exec(command)
            os.unlink(temporary_file.name)
        else:
            command += ' -r {}'.format(n + 1)
            out, err = self._exec(command)
            print(out)
            print(err)
        q = [_.split() for _ in out.split('\n') if _]
        results = []
        for x in q:
            distance = float(x[1])
            name = os.path.basename(x[0])
            event = Event.get(name=name)[0]
            if event.name != target.name:
                results.append((distance, event))
        return tuple(results[:n])

    ### PUBLIC PROPERTIES ###

    @property
    def asset_class(self):
        return self._asset_class

    @property
    def executable(self):
        from sasha import sasha_configuration
        return sasha_configuration.get_binary('audiodb')

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def name(self):
        return self._name

    @property
    def path(self):
        return self._path

    @property
    def status(self):
        out, err = self._exec('{} -d {} -S'.format(self.executable, self.path))
        lines = out.splitlines()
        lines = [_ for _ in lines if _]
        status = {}
        for line in lines:
            if line.startswith('num files'):
                status['num_files'] = int(line.partition(':')[-1])
            elif line.startswith('data dim'):
                status['data_dim'] = int(line.partition(':')[-1])
            elif line.startswith('total vectors'):
                datum = line.partition(':')[-1].split()[0]
                status['total_vectors'] = int(datum)
            elif line.startswith('vectors available'):
                datum = line.partition(':')[-1].split()[0]
                status['available_vectors'] = int(datum)
            elif line.startswith('total bytes'):
                datum = line.partition(':')[-1].split()[0]
                status['total_bytes'] = int(datum)
            elif line.startswith('bytes available'):
                datum = line.partition(':')[-1].split()[0]
                status['available_bytes'] = int(datum)
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