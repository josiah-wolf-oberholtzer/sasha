import copy
import inspect


class PluginGraph(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        '_graph',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        def _build_subtree(target, node, reservoir):
            for x in reservoir:
                if x.__requires__ == target:
                    node[x] = {}
                    _build_subtree(x, node[x], reservoir)
        from sasha.tools import assettools
        from sasha.tools.assettools.Asset import Asset
        self._client = client
        self._graph = {}
        plugins = filter(lambda x:
            hasattr(x, '__bases__') and
            Asset in inspect.getmro(x) and
            x.__client_class__ == self.client and
            not inspect.isabstract(x),
            [getattr(assettools, x) for x in dir(assettools)])
        _build_subtree(None, self._graph, plugins)

    ### PUBLIC ATTRIBUTES ###

    @property
    def client(self):
        return self._client

    @property
    def graph(self):
        return copy.deepcopy(self._graph)

    ### PUBLIC METHODS ###

    def in_order(self):
        def _depth_first(node):
            result = []
            for k, v in node.iteritems():
                result.append(k)
                if v:
                    result.extend(_depth_first(v))
            return result
        return tuple(_depth_first(self.graph))