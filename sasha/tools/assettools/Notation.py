import abc
import os
from sasha.tools.assettools.Asset import Asset
from sasha.tools.wrappertools import Convert
from sasha.tools.wrappertools import Wrapper


class Notation(Asset):

    ### CLASS VARIABLES ###

    __slots__ = ()
    _aa_factor = 4
    _resolution = 72
    file_suffix = 'png'
    media_type = 'scores'

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _make_illustration(self, sublabel):
        raise NotImplemented

    def _path_to_lily_path(self, path):
        from sasha import sasha_configuration
        path = self._strip_file_suffix(path)
        path = path.partition(sasha_configuration.get_media_path('scores'))[-1]
        return sasha_configuration.get_media_path('lilypond') + path + '.ly'

    def _path_to_ps_path(self, path):
        return self._strip_file_suffix(path) + '.ps'

    def _strip_file_suffix(self, path):
        return path.partition('.{}'.format(self.file_suffix))[0]

    def _save_lily_to_png(self, lily, sublabel=None):
        import abjad
        from sasha import sasha_configuration
        png_path = self._build_path(sublabel)
        lily_path = self._path_to_lily_path(png_path)
        suffixless_path = self._strip_file_suffix(png_path)
        ps_path = self._path_to_ps_path(png_path)
        lily_directory, _ = os.path.split(lily_path)
        if not os.path.exists(lily_directory):
            os.makedirs(lily_directory)
        png_directory, _ = os.path.split(png_path)
        if not os.path.exists(png_directory):
            os.makedirs(png_directory)
        abjad.persist(lily).as_ly(lily_path)
        cmd = '{} --png -dresolution={} -danti-alias-factor={} -o {} {}'.format(
            sasha_configuration.get_binary('lilypond'),
            self.resolution,
            self.aa_factor,
            suffixless_path,
            lily_path,
            )
        out, err = Wrapper()._exec(cmd)
        # sometimes LilyPond doesn't delete the PostScript
        if os.path.exists(ps_path):
            os.remove(ps_path)
        # sometimes LilyPond (or something else?) appends '.old'
        if os.path.exists(png_path + '.old'):
            os.remove(png_path)
            os.rename(png_path + '.old', png_path)
        Convert()(png_path, png_path)

    ### PUBLIC METHODS ###

    def delete(self, sublabel=None):
        if sublabel is None:
            if isinstance(self.path, dict):
                for path in self.path.values():
                    if os.path.exists(path):
                        os.remove(path)
            elif os.path.exists(self.path):
                os.remove(self.path)
        elif sublabel in self.plugin_sublabels:
            if os.path.exists(self.path[sublabel]):
                os.remove(self.path[sublabel])

    def write(self, sublabel=None, **kwargs):
        try:
            lily = self._make_illustration(sublabel)
            self._asset = lily
            self._save_lily_to_png(lily, sublabel)
        except:
            import sys
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print '\n'.join(traceback.format_exception(
                exc_type, exc_value, exc_traceback))

    ### PUBLIC PROPERTIES ###

    @property
    def aa_factor(self):
        return self._aa_factor

    @property
    def resolution(self):
        return self._resolution