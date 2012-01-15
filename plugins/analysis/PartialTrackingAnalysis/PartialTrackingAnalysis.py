import os
import struct
from sasha.core.plugins import _MediaPlugin
from sasha.plugins.audio.SourceAudio import SourceAudio


class PartialTrackingAnalysis(_MediaPlugin):

    __requires__ = SourceAudio

    _media = 'analyses'
    _suffix = 'partials'

    ### PRIVATE METHODS ###

    def _find_tracks(self, parallel = True, **kwargs):
        from sasha.tools.analysistools import PeakDetector
        from sasha.tools.analysistools import PartialTracker
        frames = PeakDetector(max_peak_count = 15)(SourceAudio(self), parallel = False)
        tracks = PartialTracker(min_track_length = 10)(frames)
        for track in tracks:
            for peak in track:
                peak.previous_peak = peak.next_peak = None
        return tracks

    ### PUBLIC METHODS ###

    def delete(self):
        if self.exists:
            os.remove(self.path)

    def read(self):
        from sasha.tools.analysistools import Peak
        from sasha.tools.analysistools import Track

        input = open(self.path, 'rb')
        data = input.read( )
        input.close( )

        tracks = [ ]
        byte_offset = 0
        fmt = 'i'
        num_tracks = struct.unpack_from(fmt, data, byte_offset)[0]
        byte_offset += struct.calcsize(fmt)

        for i in range(num_tracks):

            track = [ ]
            fmt = 'i'
            num_peaks = struct.unpack_from(fmt, data, byte_offset)[0]
            byte_offset += struct.calcsize(fmt)

            for j in range(num_peaks):

                fmt = 'dddi'
                frequency, amplitude, phase, frame_ID = struct.unpack_from(fmt, data, byte_offset)
                track.append(Peak(frequency, amplitude, phase, frame_ID = frame_ID))
                byte_offset += struct.calcsize(fmt)

            tracks.append(Track(track))

        object.__setattr__(self, '_asset', tuple(tracks))
        return self.asset

    def write(self, **kwargs):
        object.__setattr__(self, '_asset', self._find_tracks(kwargs))
        self.delete( )
        output = open(self.path, 'wb')

        # write the number of tracks as an int
        output.write(struct.pack('i', len(self.asset)))

        # write each track
        for track in self.asset:
            # write the number of peaks in the track as an int
            output.write(struct.pack('i', len(track)))

            # write each peak as freq, amp, phase, frame_ID 4-tuple
            for peak in track:
                output.write(struct.pack('dddi',
                    peak.frequency, peak.amplitude, peak.phase, peak.frame_ID))

        output.close( )
