import multiprocessing

from sasha import SASHA
from sasha.core.bootstrap._populate_all_assets_for_object \
    import _populate_all_assets_for_object
from sasha.core.plugins import PluginGraph


def _populate_all_assets():

    SASHA.logger.info('Populating all assets.')

    for domain_class in SASHA.get_domain_classes():
        SASHA.logger.info('Populating plugins for %s.' % domain_class.__name__)
        plugins = PluginGraph(domain_class).in_order()
        args = [(domain_class, x.id, plugins) for x in domain_class.get()]
        if args:
            if 1 < multiprocessing.cpu_count():
                pool = multiprocessing.Pool()
                pool.map_async(_populate_all_assets_for_object, args)
                pool.close()
                pool.join()
            else:
                map(_populate_all_assets_for_object, args)
