import abc
import os
from sasha.tools.systemtools import Immutable
from sasha.tools.domaintools import Event


class Asset(Immutable):

    ### CLASS ATTRIBUTES ###

    __domain_class__ = Event
    __metaclass__ = abc.ABCMeta
    __requires__ = None
    __slots__ = (
        '_asset',
        '_client',
        )

    file_suffix = None
    media_type = None
    plugin_label = None
    plugin_sublabels = ()

    ### INITIALIZER ###

    def __init__(self, arg):
        if not isinstance(arg, self.__domain_class__):
            if (
                hasattr(arg, 'client') and
                isinstance(arg.client, self.__domain_class__)
                ):
                arg = arg.client
            elif (
                isinstance(arg, (str, unicode)) and
                hasattr(self.__domain_class__, 'name')
                ):
                arg = self.__domain_class__.get(name=arg)[0]
            elif isinstance(arg, int):
                arg = self.__domain_class__.get(id=arg)[0]
            else:
                message = 'Cannot instantiate %s from %s'
                message = message % (self.__domain_class__.__name__, repr(arg))
                raise ValueError(message)
        object.__setattr__(self, '_client', arg)
        object.__setattr__(self, '_asset', None)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<%s(%s)>' % (self.__class__.__name__, repr(self.client))

    ### PRIVATE METHODS ###

    def _build_path(self, sublabel=None):
        from sasha import sasha_configuration
        name = str(self.client.canonical_name)
        if self.plugin_label:
            name += '__%s' % self.plugin_label
        if sublabel is not None and sublabel in self.plugin_sublabels:
            name += '__%s' % sublabel
        if self.file_suffix:
            name += '.%s' % self.file_suffix
        return os.path.join(sasha_configuration.get_media_path(self.media_type), name)

    ### PUBLIC PROPERTIES ###

    @property
    def asset(self):
        return self._asset

    @property
    def client(self):
        return self._client

    @property
    def exists(self):
        if isinstance(self.path, (str, unicode)):
            return os.path.exists(self.path)
        elif isinstance(self.path, dict):
            exists = {}
            for sublabel, path in self.path.iteritems():
                exists[sublabel] = os.path.exists(path)
            return exists
        raise Exception('Bad path: %s' % repr(self.path))

    @property
    def path(self):
        if len(self.plugin_sublabels):
            path = {}
            for sublabel in self.plugin_sublabels:
                path[sublabel] = self._build_path(sublabel)
            return path
        return self._build_path()