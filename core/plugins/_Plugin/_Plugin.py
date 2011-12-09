from sasha.core.domain import Event
from sasha.core.mixins import _Immutable


class _Plugin(_Immutable):

    _requires = tuple( )
    __slots__ = ('_event',)

    def __init__(self, arg):
        if not isinstance(arg, Event):
            if hasattr(arg, 'event') and isinstance(arg.event, Event):
                arg = arg.event
            else:
                try:   
                    arg = Event(arg)
                except:
                    raise ValueError('Cannot instantiate an Event from %s' % repr(arg))
        object.__setattr__(self, '_event', arg)

    ### OVERRIDES ###

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, repr(self.event.name))

    ### PUBLIC ATTRIBUTES ###

    @property
    def event(self):
        return self._event

    @property
    def requires(self):
        return self._requires


