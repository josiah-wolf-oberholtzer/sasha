from sasha import SASHA
from sasha.core.wrappers.Wrapper import Wrapper


class Playback(Wrapper):

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
        return SASHA.get_binary('playback')
