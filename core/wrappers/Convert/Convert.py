from sasha import SASHA
from sasha.core.wrappers.Wrapper import Wrapper


class Convert(Wrapper):

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
        return SASHA.get_binary('convert')



