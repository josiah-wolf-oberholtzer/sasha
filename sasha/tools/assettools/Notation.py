from __future__ import print_function
import abc
import os
from sasha.tools.assettools.Asset import Asset
from sasha.tools.executabletools import Executable


class Notation(Asset):

    ### CLASS VARIABLES ###

    __slots__ = ()
    file_suffix = 'svg'
    media_type = 'scores'

    ### SPECIAL METHODS ###

    def __illustrate__(self):
        return self._make_illustration()

    ### PRIVATE METHODS ###

    @abc.abstractmethod
    def _make_illustration(self):
        raise NotImplemented

    def _path_to_lilypond_path(self, path):
        from sasha import sasha_configuration
        _, filename = os.path.split(path)
        suffixless_filename, _ = os.path.splitext(filename)
        lilypond_directory = sasha_configuration.get_media_path('lilypond')
        lilypond_filename = suffixless_filename + '.ly'
        return os.path.join(lilypond_directory, lilypond_filename)

    def _save_lilypond_file_as_svg(self, lilypond_file):
        import abjad
        from sasha import sasha_configuration

        output_filepath = self._build_path()
        output_directory, output_filename = os.path.split(output_filepath)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        lilypond_path = self._path_to_lilypond_path(output_filepath)
        lilypond_directory, _ = os.path.split(lilypond_path)
        if not os.path.exists(lilypond_directory):
            os.makedirs(lilypond_directory)

        suffixless_filepath, _ = os.path.splitext(output_filepath)
        preview_filepath = '{}.preview.{}'.format(
            suffixless_filepath, self.file_suffix)

        abjad.persist(lilypond_file).as_ly(lilypond_path)
        command = '{} -dbackend=svg -dpreview -dno-point-and-click -o {} {}'
        command = command.format(
            sasha_configuration.get_binary('lilypond'),
            suffixless_filepath,
            lilypond_path,
            )
        out, err = Executable()._exec(command)
        if out or err:
            print(out)
            print(err)

        os.remove(output_filepath)
        os.rename(preview_filepath, output_filepath)

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
        return HTML.tag('img', src=self.get_static_path(request))

    def write(self, **kwargs):
        try:
            lilypond_file = self._make_illustration()
            self._asset = lilypond_file
            self._save_lilypond_file_as_svg(lilypond_file)
        except:
            import sys
            import traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            message = '\n'.join(
                traceback.format_exception(exc_type, exc_value, exc_traceback),
                )
            print(message)