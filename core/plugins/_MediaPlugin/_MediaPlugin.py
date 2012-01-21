import os
from sasha import SASHA
from sasha.core.plugins._Plugin import _Plugin


class _MediaPlugin(_Plugin):

    __slots__ = ('_asset', '_client')

    file_suffix = None
    media_type = None
    plugin_label = None
    plugin_sublabels = ( )

    def __init__(self, arg):
        _Plugin.__init__(self, arg)
        object.__setattr__(self, '_asset', None)

    ### PRIVATE METHODS ###

    def _build_path(self, sublabel = None):
        name = str(self.client.canonical_name)
        if self.plugin_label:
            name += '.%s' % self.plugin_label
        if sublabel is not None and sublable in self.plugin_sublabels:
            name += '__%s' % sublabel
        if self.file_suffix:
            name += '.%s' % self.file_suffix
        return os.path.join(SASHA.get_media_path(self.media_type), name)

    ### PUBLIC ATTRIBUTES ###

    @property
    def asset(self):
        return self._asset

    @property
    def exists(self):
        if isinstance(self.path, str):
            return os.path.exists(self.path)
        elif isinstance(self.path, dict):
            exists = { }
            for sublabel, path in self.path.iteritems( ):
                exists[sublabel] = os.path.exists(path)
            return exists
        raise Exception('Bad path: %s' % repr(self.path))

    @property
    def path(self):
        if len(self.plugin_sublabels):
            path = { }
            for sublabel in self.plugin_sublabels:
                path[sublabel] = self._build_path(sublabel)
            return path
        return self._build_path( )
