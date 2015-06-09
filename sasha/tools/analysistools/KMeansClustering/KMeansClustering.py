import numpy
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sasha.tools.domaintools import Cluster, Event
from sasha.tools.assettools import ChromaAnalysis, ConstantQAnalysis, MFCCAnalysis


class KMeansClustering(object):

    def __init__(self, feature='mfcc', cluster_count=4, use_pca=False):
        if feature in ['chroma', 'constant_q', 'mfcc']:
            self._feature = feature
        else:
            raise ValueError('Unknown feature name %r.' % feature)
        self._cluster_count = int(cluster_count)
        self._use_pca = bool(use_pca)

    ### SPECIAL METHODS ###

    def __call__(self):
        events, vectors = self.build_corpus()

        k_means = KMeans(
            init='k-means++',
            n_clusters=self.cluster_count,
            n_init=10,
            )

        if self.use_pca:
            vectors_r = self.decompose_vectors(vectors)
            k_means.fit(vectors_r)
        else:
            k_means.fit(vectors)

        k_means_labels = k_means.labels_

        clusters = {}
        for event, k_means_label in zip(events, k_means_labels):
            if k_means_label not in clusters:
                clusters[k_means_label] = Cluster(cluster_id=int(k_means_label) + 1, feature=self.feature)
            cluster = clusters[k_means_label]
            cluster.events.append(event)

        return clusters.values()

    def __repr__(self):
        return '%s(%r)' % (type(self).__name__, self._feature)

    ### PUBLIC ATTRIBUTES ###

    @property
    def cluster_count(self):
        return self._cluster_count

    @property
    def feature(self):
        return self._feature

    @property
    def feature_class(self):
        if self.feature == 'chroma':
            return ChromaAnalysis
        elif self.feature == 'constant_q':
            return ConstantQAnalysis
        elif self.feature == 'mfcc':
            return MFCCAnalysis

    @property
    def use_pca(self):
        return self._use_pca

    ### PUBLIC METHODS ###

    def build_corpus(self):
        events = []
        vectors = []
        for event in sorted(Event.get(), key=lambda x: x.name):
            feature = self.feature_class(event)
            analysis = feature.read()
            vector = numpy.hstack([feature.mean, feature.std])
            events.append(event)
            vectors.append(vector)
        vectors = numpy.vstack(vectors)
        vectors = preprocessing.scale(vectors)
        vectors /= vectors.max()
        return events, vectors

    def decompose_vectors(self, vectors):
        pca = PCA(n_components=2)
        return pca.fit(vectors).transform(vectors)
