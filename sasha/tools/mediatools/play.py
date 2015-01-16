from sasha import Event
from sasha.core.wrappers import Playback
from sasha.plugins.audio import CroppedAudio, MP3Audio, SourceAudio


def play(*args):

    playback = Playback()

    paths = [ ]
    for arg in args:
        if isinstance(arg, str):
            paths.append(arg)
        elif isinstance(arg, Event):
            paths.append(SourceAudio(arg).path)
        elif isinstance(arg, (CroppedAudio, MP3Audio, SourceAudio)):
            paths.append(arg.path)

    playback("%s" % ' '.join(paths))
