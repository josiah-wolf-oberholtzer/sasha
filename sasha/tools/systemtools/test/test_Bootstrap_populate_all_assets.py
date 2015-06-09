import py.test

from sasha import *    
from sasha.tools.systemtools import Bootstrap
from sasha.tools.assettools import PluginGraph


SASHA.environment = 'testing'

py.test.skip('Rebuilding assets is slow.')
def test_Bootstrap_populate_all_assets_01():
    bootstrap = Bootstrap()
    bootstrap.delete_sqlite_database()
    bootstrap.create_sqlite_database()
    bootstrap.populate_sqlite_primary()

    assert 0 < SASHA.get_session().query(Event).count()

    bootstrap.delete_all_assets()
    bootstrap.populate_all_assets()
    for domain_class in SASHA.get_domain_classes():
        plugins = PluginGraph(domain_class).in_order()
        for instance in domain_class.get():
            for plugin in plugins:
                exists = plugin(instance).exists
                if isinstance(exists, bool):
                    assert exists
                elif isinstance(exists, dict):
                    assert all([exists.values()])
