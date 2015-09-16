import abc
import os
from pyramid.url import static_path


class Asset(object):

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta
    __requires__ = None
    __slots__ = (
        '_asset',
        '_client',
        )
    file_suffix = None
    media_type = None
    asset_label = None

    ### INITIALIZER ###

    def __init__(self, expr):
        from sasha.tools import modeltools
        if isinstance(expr, modeltools.Event):
            client = expr
        elif isinstance(expr, Asset):
            client = expr.client
        elif isinstance(expr, (str, unicode)):
            client = modeltools.Event.objects.get(name=expr)
        elif isinstance(expr, int):
            client = modeltools.Event.objects[expr]
        else:
            message = 'Cannot instantiate {} from {!r}'
            message = message.format(type(self), expr)
            raise ValueError(message)
        self._client = client
        self._asset = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<{}({!r})>'.format(self.__class__.__name__, self.client)

    ### PRIVATE METHODS ###

    def _build_path(self):
        from sasha import sasha_configuration
        name = str(self.client.canonical_event_name)
        if self.asset_label:
            name += '__{}'.format(self.asset_label)
        if self.file_suffix:
            name += '.{}'.format(self.file_suffix)
        media_path = sasha_configuration.get_media_path(self.media_type)
        build_path = os.path.join(media_path, name)
        return build_path

    ### PUBLIC METHODS ###

    def get_static_path(self, request):
        return static_path(self.static_path, request)

    ### PUBLIC PROPERTIES ###

    @property
    def asset(self):
        return self._asset

    @property
    def client(self):
        return self._client

    @property
    def exists(self):
        return os.path.exists(self.path)

    @property
    def path(self):
        return self._build_path()

    @property
    def static_path(self):
        from sasha import sasha_configuration
        environment, path = self.path.partition(
            sasha_configuration.environment,
            )[1:]
        return 'sasha:sashamedia/%s%s' % (environment, path)