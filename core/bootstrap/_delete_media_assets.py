from inspect import getmro
from sasha import plugins
from sasha.core.domain import Event

def _delete_media_assets( ):

    events = Event.get( )
    
    klasses = [eval('plugins.' + x) \
        for x in filter(lambda x: not x.startswith('_'), dir(plugins))]
    klasses = filter(lambda x: hasattr(x, 'delete'), klasses)

    for event in events:
        for klass in klasses:
            klass(event).delete( )
