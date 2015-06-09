from sasha.core.wrappers.Wrapper import Wrapper


class Convert(Wrapper):

    ### INITIALIZER ###

    def __init__(self):
        import os
        from sasha.core.wrappers import Which
        if not os.path.isabs(self.executable):
            assert Which()('convert') is not None

    ### OVERRIDES ###

    def __call__(self, input, output):
        cmd = '%s %s -trim %s' % \
            (self.executable,
            input,
            output)
        out, err = self._exec(cmd)

    ### PUBLIC ATTRIBUTES ###

    @property
    def executable(self):
        from sasha import SASHA
        return SASHA.get_binary('convert')