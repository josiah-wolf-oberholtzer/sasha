import logging
import multiprocessing
from sasha import Event
from sasha.core.bootstrap._create_media_assets_for_event \
    import _create_media_assets_for_event


def _create_media_assets(klasses = [ ]):

    print 'CREATING MEDIA ASSETS:'

    args = [[event, klasses] for event in Event.get( )]

    multiprocessing.log_to_stderr(logging.INFO)

    if 1 < multiprocessing.cpu_count( ):
        pool = multiprocessing.Pool( )
        pool.map_async(_create_media_assets_for_event, args)
        pool.close( )
        pool.join( )
    else:
        map(_create_media_assets_for_event, args)
