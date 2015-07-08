import numpy
from sasha.tools import assettools
from sasha.tools import domaintools
from sasha.tools import newdomaintools


class KMeansClustering(object):

    ### INITIALIZER ###

    def __init__(
        self,
        feature='mfcc',
        cluster_count=4,
        use_pca=False,
        ):
        assert feature in ('chroma', 'constant_q', 'mfcc'), feature
        self._feature = feature
        self._cluster_count = int(cluster_count)
        self._use_pca = bool(use_pca)

    ### SPECIAL METHODS ###

    def __call__(self, use_mongodb=False):
        from sklearn.cluster import KMeans
        events, vectors = self.build_corpus(use_mongodb=use_mongodb)
        k_means = KMeans(
            init='k-means++',
            n_clusters=self.cluster_count,
            n_init=10,
            random_state=23,
            )
        if self.use_pca:
            vectors_r = self.decompose_vectors(vectors)
            k_means.fit(vectors_r)
        else:
            k_means.fit(vectors)
        k_means_labels = k_means.labels_
        clusters = {}
        if use_mongodb:
            cluster_class = newdomaintools.Cluster
        else:
            cluster_class = domaintools.Cluster
        for event, k_means_label in zip(events, k_means_labels):
            if k_means_label not in clusters:
                clusters[k_means_label] = cluster_class(
                    cluster_id=int(k_means_label) + 1,
                    feature=self.feature,
                    )
            cluster = clusters[k_means_label]
            cluster.events.append(event)
        return clusters.values()

    def __repr__(self):
        return '{}({!r})'.format(type(self).__name__, self._feature)

    ### PUBLIC METHODS ###

    def build_corpus(self, use_mongodb=False):
        from sklearn import preprocessing
        vectors = []
        if use_mongodb:
            events = newdomaintools.Event.objects
        else:
            events = domaintools.Event.get()
        events = sorted(events, key=lambda x: x.name)
        for event in events:
            feature = self.feature_class(event.name)
            feature.read()
            vector = numpy.hstack([feature.mean, feature.std])
            vectors.append(vector)
        vectors = numpy.vstack(vectors)
        vectors = preprocessing.scale(vectors)
        vectors /= vectors.max()
        return events, vectors

    def decompose_vectors(self, vectors):
        from sklearn.decomposition import PCA
        pca = PCA(n_components=2)
        return pca.fit(vectors).transform(vectors)

    ### PUBLIC PROPERTIES ###

    @property
    def cluster_count(self):
        return self._cluster_count

    @property
    def feature(self):
        return self._feature

    @property
    def feature_class(self):
        if self.feature == 'chroma':
            return assettools.ChromaAnalysis
        elif self.feature == 'constant_q':
            return assettools.ConstantQAnalysis
        elif self.feature == 'mfcc':
            return assettools.MFCCAnalysis

    @property
    def use_pca(self):
        return self._use_pca