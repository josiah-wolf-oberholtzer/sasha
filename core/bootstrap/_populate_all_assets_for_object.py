import sys
import traceback

from sasha import *


def _populate_all_assets_for_object(args):

    domain_class   = args[0]
    object_id      = args[1]
    plugin_classes = args[2]

    obj = domain_class.get_one(id=object_id)

    for plugin_class in plugin_classes:
        plugin = plugin_class(obj)
        try:
            if hasattr(plugin, 'write'):
                SASHA.logger.info('Writing %s.' % plugin)
                plugin.write(parallel=False)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            exc = traceback.print_exc()
            SASHA.logger.warning('Writing %s failed.' % plugin)
            if exc:
                SASHA.logger.warning('\n' + exc)
