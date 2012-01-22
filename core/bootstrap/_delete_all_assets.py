from sasha import *
from sasha.core.plugins import PluginGraph


def _delete_all_assets( ):

    SASHA.logger.info('Deleting all assets.')

    for klass in SASHA.get_domain_classes( ):
        plugins = PluginGraph(klass).in_order( )
        for instance in klass.get( ):
            for plugin in plugins:
                if hasattr(plugin, 'delete'):
                    plugin(instance).delete( )
