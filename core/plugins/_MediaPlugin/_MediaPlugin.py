import os
from sasha import SASHACFG
from sasha.core.plugins._Plugin import _Plugin


class _MediaPlugin(_Plugin):

    __slots__ = ('_asset', '_client')

    _label = None
    _media = None
    _sublabels = ( )
    _suffix = None

    def __init__(self, arg):
        _Plugin.__init__(self, arg)
        object.__setattr__(self, '_asset', None)

    ### PRIVATE METHODS ###

    def _build_path(self, sublabel = None):
        name = str(self.client.name)
        if self.label:
            name += '.%s' % self.label
        if sublabel is not None and len(sublabel):
            name += '__%s' % sublabel
        if self.suffix:
            name += '.%s' % self.suffix
        return os.path.join(SASHACFG.get_media_path(self.media), name)

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
    def label(self):
        return self._label

    @property
    def media(self):
        return self._media

    @property
    def path(self):
        if len(self.sublabels):
            path = { }
            for sublabel in self.sublabels:
                path[sublabel] = self._build_path(sublabel)
            return path
        return self._build_path( )

    @property
    def sublabels(self):
        return self._sublabels

    @property
    def suffix(self):
        return self._suffix
