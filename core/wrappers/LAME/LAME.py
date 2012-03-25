from sasha import SASHA
from sasha.core.wrappers.Wrapper import Wrapper


class LAME(Wrapper):

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

