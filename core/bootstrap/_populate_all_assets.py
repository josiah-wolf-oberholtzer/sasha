import multiprocessing

from sasha import SASHA
from sasha.core.bootstrap._populate_all_assets_for_object \
    import _populate_all_assets_for_object
from sasha.core.plugins import PluginGraph


def _populate_all_assets( ):

    SASHA.logger.info('Populating all assets.')

    for domain_class in SASHA.get_domain_classes( ):
        plugins = PluginGraph(domain_class).in_order( )
        args = [[domain_class, x.id, plugins] for x in domain_class.get( )]
        if args:
            if 1 < multiprocessing.cpu_count( ):
                pool = multiprocessing.Pool( )
                pool.map_async(_create_media_assets_for_event, args)
                pool.close( )
                pool.join( )
            else:
                map(_create_media_assets_for_event, ar
