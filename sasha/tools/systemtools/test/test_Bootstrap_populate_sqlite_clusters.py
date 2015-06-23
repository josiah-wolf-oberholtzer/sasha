from sasha import sasha_configuration
from sasha.tools import domaintools
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_sqlite_clusters_01():

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()
    bootstrap.populate_sqlite_clusters()

    clusters = domaintools.Cluster.get()
    assert clusters

    for cluster in clusters:
        assert len(cluster.events)

    bootstrap.rebuild_sqlite_database()