from sasha import SASHACFG
from sasha.core.wrappers._Wrapper import _Wrapper


class Playback(_Wrapper):

    ### OVERRIDES ###

    def __call__(self, input):
        cmd = '%s %s' % \
           (self.executable, input)
        out, err = self._exec(cmd)
        if err:
            print err

    ### PUBLIC ATTRIBUTES ###

    @property
    def executable(self):
        return SASHACFG.get_binary('playback')
