from sasha.tools.wrappertools.Wrapper import Wrapper


class Playback(Wrapper):

    ### SPECIAL METHODS ###

    def __call__(self, input_path):
        cmd = '{} {}'.format(self.executable, input_path)
        out, err = self._exec(cmd)
        if err:
            print err

    ### PUBLIC PROPERTIES ###

    @property
    def executable(self):
        from sasha import sasha_configuration
        return sasha_configuration.get_binary('playback')