import os
from sasha import SASHACFG
from sasha.core.plugins._MediaPlugin import _MediaPlugin
from sasha.core.wrappers import Convert
from sasha.core.wrappers import _Wrapper


class _Notation(_MediaPlugin):

    _aa_factor = 4
    _resolution = 72
    _media = 'scores'
    _suffix = 'png'

    ### PRIVATE METHODS ###

    def _path_to_lily_path(self, path):
        path = path.rpartition(self.suffix)[0]
        path = path.partition(SASHACFG.get_media_path('scores'))[-1]
        return SASHACFG.get_media_path('lilypond') + path + 'ly'

    def _path_to_pdf_path(self, path):
        path = path.rpartition(self.suffix)[0]
        return path + 'pdf'

    def _path_to_suffixless_path(self, path):
        return path.partition('.%s' % self.suffix)[0]

    def _save_lily_to_png(self, lily, sublabel = None):
        from abjad.tools.iotools import write_expr_to_ly
        lily_path = self._path_to_lily_path(self._build_path(sublabel))
        suffixless_path = self._path_to_suffixless_path(self._build_path(sublabel))
        png_path = self._build_path(sublabel)
        write_expr_to_ly(lily, lily_path, print_status = False)
        cmd = '%s --png -dresolution=%d -danti-alias-factor=%d -o %s %s' % \
            (SASHACFG.get_binary('lilypond'),
            self.resolution,
            self.aa_factor,
            suffixless_path,
            lily_path)
        out, err = _Wrapper( )._exec(cmd)
        Convert( )(png_path, png_path)

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
            for path in self.path.keys( ):
                if os.path.exists(path):
                    os.remove(path)
        elif sublabel in self.sublabels:
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
            exc_type, exc_value, exc_traceback = sys.exc_info( )
            print '\n'.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
