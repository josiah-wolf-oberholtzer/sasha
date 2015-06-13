from sasha.tools.wrappertools.Wrapper import Wrapper


class Convert(Wrapper):

    ### INITIALIZER ###

    def __init__(self):
        import os
        from sasha.tools.wrappertools import Which
        if not os.path.isabs(self.executable):
            assert Which()('convert') is not None

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