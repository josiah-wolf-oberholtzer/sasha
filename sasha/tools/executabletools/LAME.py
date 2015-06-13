import os
from sasha.tools.executabletools.Executable import Executable


class LAME(Executable):

    ### INITIALIZER ###

    def __init__(self):
        from sasha import sasha_configuration
        import os
        executable = sasha_configuration.get_binary('lame')
        if not os.path.isabs(executable):
            path = sasha_configuration.find_executable(executable)
            assert path is not None

    ### SPECIAL METHODS ###

    def __call__(self, input_path, output_path):
        from sasha import sasha_configuration
        executable = sasha_configuration.get_binary('lame')
        output_path = os.path.abspath(output_path)
        out_directory, _ = os.path.split(output_path)
        if not os.path.exists(out_directory):
            os.makedirs(out_directory)
        command = '{} -V0 {} {}'.format(
            executable,
            input_path,
            output_path,
            )
        out, err = self._exec(command)