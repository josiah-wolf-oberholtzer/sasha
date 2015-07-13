import abc
import os
from sasha.tools.assettools.Asset import Asset
from sasha.tools.executabletools import Convert
from sasha.tools.executabletools import Executable


class Notation(Asset):

    ### CLASS VARIABLES ###

    __slots__ = ()
    file_suffix = 'png'
    media_type = 'scores'

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _make_illustration(self):
        raise NotImplemented

    def _path_to_lilypond_path(self, path):
        from sasha import sasha_configuration
        path = self._strip_file_suffix(path)
        path = path.partition(sasha_configuration.get_media_path('scores'))[-1]
        return sasha_configuration.get_media_path('lilypond') + path + '.ly'

    def _path_to_ps_path(self, path):
        return self._strip_file_suffix(path) + '.ps'

    def _strip_file_suffix(self, path):
        return path.partition('.{}'.format(self.file_suffix))[0]

    def _save_lilypond_file_as_png(self, lilypond_file):
        import abjad
        from sasha import sasha_configuration
        output_path = self._build_path()
        lilypond_path = self._path_to_lilypond_path(output_path)
        suffixless_path = self._strip_file_suffix(output_path)
        lilypond_directory, _ = os.path.split(lilypond_path)
        if not os.path.exists(lilypond_directory):
            os.makedirs(lilypond_directory)
        png_directory, _ = os.path.split(output_path)
        if not os.path.exists(png_directory):
            os.makedirs(png_directory)
        abjad.persist(lilypond_file).as_ly(lilypond_path)
        command = '{} --png -dresolution=72 -danti-alias-factor=4 -o {} {}'
        command = command.format(
            sasha_configuration.get_binary('lilypond'),
            suffixless_path,
            lilypond_path,
            )
        out, err = Executable()._exec(command)
        Convert()(output_path, output_path)

    ### PUBLIC METHODS ###

    def delete(self):
        if os.path.exists(self.path):
            os.remove(self.path)

    def get_image_link(self, request):
        from webhelpers.html import HTML
        href = self.client.get_url(request)
        content = self.get_image_tag(request)
        return HTML.tag('a', href=href, c=content)

    def get_image_tag(self, request):
        from webhelpers.html import HTML
        return HTML.tag('img', src=self.get_static_url(request))

    def write(self, **kwargs):
        try:
            lilypond_file = self._make_illustration()
            self._asset = lilypond_file
            self._save_lilypond_file_as_png(lilypond_file)
        except:
            import sys
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print '\n'.join(traceback.format_exception(
                exc_type, exc_value, exc_traceback))