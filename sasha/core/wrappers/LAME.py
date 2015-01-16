from sasha import SASHA
from sasha.core.wrappers.Wrapper import Wrapper


class LAME(Wrapper):

    ### INITIALIZER ###

    def __init__(self):
        import os
        from sasha.core.wrappers import Which
        if not os.path.isabs(self.executable):
            assert Which()('lame') is not None

    ### OVERRIDES ###

    def __call__(self, input, output):
        cmd = '%s -V0 %s %s' % \
           (self.executable, input, output)
        out, err = self._exec(cmd)
        #if err:
        #    print err
        #if out:
        #    print out

    ### PUBLIC ATTRIBUTES ###

    @property
    def executable(self):
        return SASHA.get_binary('lame')

