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
        return '<%s(cluster_id=%d, feature=%r)>' % (type(self).__name__, self.cluster_id, self.feature)
