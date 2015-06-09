from abc import ABCMeta
from abjad.tools import stringtools
from sasha.tools.systemtools import Immutable
from sasha.tools.domaintools import Event


class _Plugin(Immutable):

    ### CLASS ATTRIBUTES ###
    
    __client_class__ = Event
    __requires__ = None
    __slots__ = ('_client',)

    ### INITIALIZER ###

    def __init__(self, arg):

        if not isinstance(arg, self.__client_class__):
            client_class_name = stringtools.to_snake_case(self.__client_class__.__name__)
            if hasattr(arg, 'client') and isinstance(arg.client, self.__client_class__):
                arg = arg.client

            elif isinstance(arg, (str, unicode)) and hasattr(self.__client_class__, 'name'):
                arg = self.__client_class__.get(name=arg)[0]

            elif isinstance(arg, int):
                arg = self.__client_class__.get(id=arg)[0]

            else:
                raise ValueError('Cannot instantiate %s from %s' % (self.__client_class__.__name__, repr(arg)))

        object.__setattr__(self, '_client', arg)

    ### OVERRIDES ###

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, repr(self.client))

    ### PUBLIC ATTRIBUTES ###

    @property
    def client(self):
        return self._client

    @property
    def requires(self):
        return self._requires

