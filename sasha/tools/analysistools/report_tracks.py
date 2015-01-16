from abjad.tools import pitchtools


def report_tracks(tracks):
    max_amp = sorted(tracks, key = lambda x: x.amplitude_mean, reverse = True)[0].amplitude_mean
    for track in sorted(tracks, key = lambda x: x.db(max_amp)):
        print '%d \t[%d:%d]  \t%f \t%0.1f \t%s' % (
            len(track), 
            track.start_frame,
            track.stop_frame, 
            track.db(max_amp), 
            track.semitones_centroid, 
            pitchtools.NamedPitch(track.semitones_centroid).format)
