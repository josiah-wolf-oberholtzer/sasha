from sasha.tools.wrappertools.Wrapper import Wrapper


class Convert(Wrapper):

    ### INITIALIZER ###

    def __init__(self):
        import os
        from sasha.tools.wrappertools import Which
        if not os.path.isabs(self.executable):
            assert Which()('convert') is not None

    ### SPECIAL METHODS ###

    def __call__(self, input, output):
        cmd = '%s %s -trim %s' % \
            (self.executable,
            input,
            output)
        out, err = self._exec(cmd)

    ### PUBLIC PROPERTIES ###

    @property
    def executable(self):
        from sasha import sasha_configuration
        return sasha_configuration.get_binary('convert')