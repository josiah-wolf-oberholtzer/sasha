from abc import ABCMeta
from sasha.tools.systemtools import Immutable
from sasha.tools.domaintools import Event


class Asset(Immutable):

    ### CLASS ATTRIBUTES ###

    __client_class__ = Event
    __requires__ = None
    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, arg):
        if not isinstance(arg, self.__client_class__):
            if (
                hasattr(arg, 'client') and
                isinstance(arg.client, self.__client_class__)
                ):
                arg = arg.client
            elif (
                isinstance(arg, (str, unicode)) and
                hasattr(self.__client_class__, 'name')
                ):
                arg = self.__client_class__.get(name=arg)[0]
            elif isinstance(arg, int):
                arg = self.__client_class__.get(id=arg)[0]
            else:
                message = 'Cannot instantiate %s from %s'
                message = message % (self.__client_class__.__name__, repr(arg))
                raise ValueError(message)
        object.__setattr__(self, '_client', arg)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, repr(self.client))

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def requires(self):
        return self._requires