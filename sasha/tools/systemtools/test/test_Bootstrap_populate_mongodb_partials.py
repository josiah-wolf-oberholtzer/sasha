from sasha import sasha_configuration
from sasha.tools import models
from sasha.tools import systemtools


sasha_configuration.environment = 'testing'


def test_Bootstrap_populate_mongodb_partials_01():

    bootstrap = systemtools.Bootstrap()
    bootstrap.delete_mongodb_database()
    bootstrap.create_mongodb_database()
    bootstrap.populate_mongodb_primary()
    bootstrap.populate_mongodb_partials()

    for event in models.Event.objects:
        assert event.partials

    bootstrap.rebuild_mongodb_database()