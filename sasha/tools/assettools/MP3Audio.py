import os
from sasha.tools.assettools.Asset import Asset
from sasha.tools.assettools.SourceAudio import SourceAudio
from sasha.tools.executabletools import LAME
from sasha.tools.executabletools import Playback


class MP3Audio(Asset):

    ### CLASS VARIABLES ###

    __requires__ = SourceAudio
    __slots__ = ()
    file_suffix = 'mp3'
    media_type = 'mp3s'

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def get_audio_tag(self, request):
        from webhelpers.html import HTML
        static_url = self.get_static_url(request)
        source_tag = HTML.tag('source', type_='audio/mp3', src=static_url)
        audio_tag = HTML.tag('audio', controls='controls', c=[source_tag])
        div_tag = HTML.tag('div', class_='mp3', c=[audio_tag])
        return div_tag

    def playback(self):
        Playback()(self.path)

    def write(self, **kwargs):
        LAME()(SourceAudio(self).path, self.path)