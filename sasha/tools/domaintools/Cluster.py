from sqlalchemy import Column, Integer, String
from sasha.tools.domaintools.DomainObject import DomainObject


class Cluster(DomainObject):

    ### SQLALCHEMY ###

#    __table_args__ = (UniqueConstraint('cluster', 'feature'), {})

    cluster_id = Column(Integer)
    feature = Column(String(32))
    technique = Column(String(32))

    ### SPECIAL METHODS ###

    def __repr__(self):
        result = '<{}(cluster_id={}, feature={!r})>'
        result = result.format(
            type(self).__name__,
            self.cluster_id,
            self.feature,
            )
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        if self.feature == 'mfcc':
            return 'MFCC'
        elif self.feature == 'constant_q':
            return 'Constant-Q'
        elif self.feature == 'chroma':
            return 'Chroma'
        raise ValueError
