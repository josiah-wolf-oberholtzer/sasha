import copy
import inspect


class PluginGraph(object):

    __slots__ = ('_client', '_graph')

    def __init__(self, client):
        from sasha import plugins
        from sasha.core.plugins._Plugin import _Plugin

        self._client = client
        self._graph = { } 

        plugins = filter(lambda x:
            hasattr(x, '__bases__') and
            _Plugin in inspect.getmro(x) and 
            x.__client_class__ == self.client,
            [getattr(plugins, x) for x in dir(plugins)])

        def _build_subtree(target, node, reservoir):
            '''Loop through reservoir.  If a plugin's __requires__
            is equal to target, add that plugin as a key in node,
            and call this function recursively on that new node.'''

            for x in reservoir:
                if x.__requires__ == target:
                    node[x] = { }
                    _build_subtree(x, node[x], reservoir)

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
            result = [ ]
            for k, v in node.iteritems( ):
                result.append(k)
                if v:
                    result.extend(_depth_first(v))
            return result

        return tuple(_depth_first(self.graph))
