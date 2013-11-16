from abjad.tools import pitchtools

from sasha import *
from sasha.plugins import ChordAnalysis
from sasha.tools.analysistools import KMeansClustering


def _populate_sqlite_secondary():

    SASHA.logger.info('Populate SQLite secondary objects.')

    session = SASHA.get_session()

    # insert Partials
    for event in Event.get():
        chord = ChordAnalysis(event).read()
        for pitch_number, amplitude in chord:
            pitch = pitchtools.NamedPitch(pitch_number)
            pitch_class_number = pitch.chromatic_pitch_class_number
            octave_number = pitch.octave_number
            session.add(Partial(event_id=event.id,
                pitch_number=pitch_number,
                pitch_class_number=pitch_class_number,
                octave_number=octave_number,
                amplitude=amplitude))
        session.commit()

    # insert Clusters
    chroma_kmeans = KMeansClustering('chroma', cluster_count=8, use_pca=False)
    constant_q_kmeans = KMeansClustering('constant_q', cluster_count=8, use_pca=False)
    mfcc_kmeans = KMeansClustering('mfcc', cluster_count=8, use_pca=False)
    all_clusters = [ ]
    all_clusters.extend(chroma_kmeans())
    all_clusters.extend(constant_q_kmeans())
    all_clusters.extend(mfcc_kmeans())
    for cluster in all_clusters:
        session.merge(cluster)
    session.commit()
