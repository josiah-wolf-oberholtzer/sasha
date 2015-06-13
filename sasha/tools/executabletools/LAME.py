import os
from sasha.tools.executabletools.Executable import Executable


class LAME(Executable):

    ### INITIALIZER ###

    def __init__(self):
        import os
        from sasha.tools.executabletools import Which
        if not os.path.isabs(self.executable):
            assert Which()('lame') is not None

    ### SPECIAL METHODS ###

    def __call__(self, input_, output):
        output = os.path.abspath(output)
        out_directory, _ = os.path.split(output)
        if not os.path.exists(out_directory):
            os.makedirs(out_directory)
        command = '{} -V0 {} {}'.format(
            self.executable,
            input_,
            output,
            )
        out, err = self._exec(command)

    ### PUBLIC PROPERTIES ###

    @property
    def executable(self):
        from sasha import sasha_configuration
        return sasha_configuration.get_binary('lame')