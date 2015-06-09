import py.test

from sasha import *    
from sasha.tools.systemtools import Bootstrap
from sasha.tools.assettools import PluginGraph


sasha_configuration.environment = 'testing'

py.test.skip('Rebuilding assets is slow.')
def test_Bootstrap_delete_all_assets_01():
    bootstrap = Bootstrap()
    bootstrap.delete_all_assets()
    for domain_class in sasha_configuration.get_domain_classes():
        plugins = PluginGraph(domain_class).in_order()
        for instance in domain_class.get():
            for plugin in plugins:
                exists = plugin(instance).exists
                if isinstance(exists, bool):
                    assert not exists
                elif isinstance(exists, dict):
                    assert all([not x for x in exists.values()])
