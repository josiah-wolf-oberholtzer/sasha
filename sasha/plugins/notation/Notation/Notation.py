import abc
import os
from sasha import SASHA
from sasha.core.plugins._MediaPlugin import _MediaPlugin
from sasha.core.wrappers import Convert
from sasha.core.wrappers import Wrapper


class Notation(_MediaPlugin):

    _aa_factor = 4
    _resolution = 72
    media_type = 'scores'
    file_suffix = 'png'

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _build_lily(self, sublabel):
        raise NotImplemented

    def _path_to_lily_path(self, path):
        path = self._strip_file_suffix(path)
        path = path.partition(SASHA.get_media_path('scores'))[-1]
        return SASHA.get_media_path('lilypond') + path + '.ly'

    def _path_to_ps_path(self, path):
        return self._strip_file_suffix(path) + '.ps'

    def _strip_file_suffix(self, path):
        return path.partition('.%s' % self.file_suffix)[0]

    def _save_lily_to_png(self, lily, sublabel = None):
        import abjad

        png_path = self._build_path(sublabel)
        lily_path = self._path_to_lily_path(png_path)
        suffixless_path = self._strip_file_suffix(png_path)
        ps_path = self._path_to_ps_path(png_path)

        abjad.persist(lily).as_ly(lily_path)
        #iotools.write_expr_to_ly(lily, lily_path, print_status = False)
        cmd = '%s --png -dresolution=%d -danti-alias-factor=%d -o %s %s' % \
            (SASHA.get_binary('lilypond'),
            self.resolution,
            self.aa_factor,
            suffixless_path,
            lily_path)
        out, err = Wrapper()._exec(cmd)

        # sometimes LilyPond doesn't delete the PostScript
        if os.path.exists(ps_path):
            os.remove(ps_path)

        # sometimes LilyPond (or something else?) appends '.old'
        if os.path.exists(png_path + '.old'):
            os.remove(png_path)
            os.rename(png_path + '.old', png_path)

        Convert()(png_path, png_path)

    ### PUBLIC ATTRIBUTES ###

    @property
    def aa_factor(self):
        return self._aa_factor

    @property
    def resolution(self):
        return self._resolution

    ### PUBLIC METHODS ###

    def delete(self, sublabel = None):
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

    def write(self, sublabel = None, **kwargs):
        try:
            lily = self._build_lily(sublabel)
            object.__setattr__(self, '_asset', lily)
            self._save_lily_to_png(lily, sublabel)
        except:
            import sys
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
