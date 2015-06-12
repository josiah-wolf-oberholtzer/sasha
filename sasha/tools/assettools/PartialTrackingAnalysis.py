import os
import struct
from sasha.tools.assettools.Asset import Asset
from sasha.tools.assettools.SourceAudio import SourceAudio


class PartialTrackingAnalysis(Asset):

    ### CLASS VARIABLES ###

    __requires__ = SourceAudio

    media_type = 'analyses'
    file_suffix = 'partials'

    ### PRIVATE METHODS ###

    def _find_tracks(self, parallel=False, **kwargs):
        from sasha.tools.analysistools import PeakDetector
        from sasha.tools.analysistools import PartialTracker
        peak_detector = PeakDetector(max_peak_count=15)
        frames = peak_detector(SourceAudio(self), parallel=False)
        tracks = PartialTracker(min_track_length=10)(frames)
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
        with open(self.path, 'rb') as file_pointer:
            data = file_pointer.read()
        tracks = []
        byte_offset = 0
        num_tracks = struct.unpack_from('i', data, byte_offset)[0]
        byte_offset += struct.calcsize('i')
        for i in range(num_tracks):
            track = []
            num_peaks = struct.unpack_from('i', data, byte_offset)[0]
            byte_offset += struct.calcsize('i')
            for j in range(num_peaks):
                frequency, amplitude, phase, frame_id = struct.unpack_from(
                    'dddi', data, byte_offset)
                peak = Peak(frequency, amplitude, phase, frame_id=frame_id)
                track.append(peak)
                byte_offset += struct.calcsize('dddi')
            tracks.append(Track(track))
        self._asset = tuple(tracks)
        return self.asset

    def write(self, **kwargs):
        self._asset = self._find_tracks(kwargs)
        self.delete()
        output_directory, _ = os.path.split(self.path)
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        with open(self.path, 'wb') as file_pointer:
            # write the number of tracks as an int
            file_pointer.write(struct.pack('i', len(self.asset)))
            # write each track
            for track in self.asset:
                # write the number of peaks in the track as an int
                file_pointer.write(struct.pack('i', len(track)))
                # write each peak as freq, amp, phase, frame_id 4-tuple
                for peak in track:
                    packed = struct.pack(
                        'dddi',
                        peak.frequency,
                        peak.amplitude,
                        peak.phase,
                        peak.frame_id,
                        )
                    file_pointer.write(packed)