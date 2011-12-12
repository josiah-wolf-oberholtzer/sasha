from sasha import SASHACFG
from sasha.core.wrappers._Wrapper import _Wrapper


class LAME(_Wrapper):

    ### OVERRIDES ###

    def __call__(self, input, output):
        cmd = '%s -V0 %s %s' % \
           (self.executable, input, output)
        out, err = self._exec(cmd)    

    ### PUBLIC ATTRIBUTES ###

    @property
    def executable(self):
        return SASHACFG.get_binary('lame')
