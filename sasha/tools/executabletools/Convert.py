from sasha.tools.executabletools.Executable import Executable


class Convert(Executable):

    ### INITIALIZER ###

    def __init__(self):
        import os
        if not os.path.isabs(self.executable):
            assert Executable.find_executable('convert') is not None

    ### SPECIAL METHODS ###

    def __call__(self, input_path, output_path):
        cmd = '{} {} -trim {}'.format(
            self.executable,
            input_path,
            output_path,
            )
        out, err = self._exec(cmd)

    ### PUBLIC PROPERTIES ###

    @property
    def executable(self):
        from sasha import sasha_configuration
        return sasha_configuration.get_binary('convert')