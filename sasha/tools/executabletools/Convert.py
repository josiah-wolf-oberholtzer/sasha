from sasha.tools.executabletools.Executable import Executable


class Convert(Executable):

    ### INITIALIZER ###

    def __init__(self):
        from sasha import sasha_configuration
        import os
        executable = sasha_configuration.get_binary('convert')
        if not os.path.isabs(executable):
            path = sasha_configuration.find_executable(executable)
            assert path is not None

    ### SPECIAL METHODS ###

    def __call__(self, input_path, output_path):
        from sasha import sasha_configuration
        executable = sasha_configuration.get_binary('convert')
        command = '{} {} -trim {}'.format(
            executable,
            input_path,
            output_path,
            )
        out, err = self._exec(command)