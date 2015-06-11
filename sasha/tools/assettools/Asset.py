import abc
import os
from sasha.tools.domaintools import Event


class Asset(object):

    ### CLASS VARIABLES ###

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

    def __init__(self, expr):
        if isinstance(expr, self.__domain_class__):
            client = expr
        elif (
            hasattr(expr, 'client') and
            isinstance(expr.client, self.__domain_class__)
            ):
            client = expr.client
        elif (
            isinstance(expr, (str, unicode)) and
            hasattr(self.__domain_class__, 'name')
            ):
            client = self.__domain_class__.get(name=expr)[0]
        elif isinstance(expr, int):
            client = self.__domain_class__.get(id=expr)[0]
        else:
            message = 'Cannot instantiate {} from {!r}'
            message = message.format(self.__domain_class__.__name__, expr)
            raise ValueError(message)
        self._client = client
        self._asset = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__, self.client)

    ### PRIVATE METHODS ###

    def _build_path(self, sublabel=None):
        from sasha import sasha_configuration
        name = str(self.client.canonical_name)
        if self.plugin_label:
            name += '__{}'.format(self.plugin_label)
        if sublabel is not None and sublabel in self.plugin_sublabels:
            name += '__{}'.format(sublabel)
        if self.file_suffix:
            name += '.{}'.format(self.file_suffix)
        media_path = sasha_configuration.get_media_path(self.media_type)
        build_path = os.path.join(media_path, name)
        return build_path

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
        message = 'Bad path: {!r}'.format(self.path)
        raise Exception(message)

    @property
    def path(self):
        if len(self.plugin_sublabels):
            path = {}
            for sublabel in self.plugin_sublabels:
                path[sublabel] = self._build_path(sublabel)
            return path
        return self._build_path()