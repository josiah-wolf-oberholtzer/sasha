import copy
import inspect


class AssetDependencyGraph(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_childwise_graph',
        '_domain_class',
        '_parentwise_graph',
        )

    ### INITIALIZER ###

    def __init__(self, domain_class):
        from sasha.tools import assettools
        from sasha.tools.assettools.Asset import Asset
        self._domain_class = domain_class
        self._childwise_graph = {}
        for asset_class_name in dir(assettools):
            asset_class = getattr(assettools, asset_class_name)
            if asset_class is Asset:
                continue
            if not isinstance(asset_class, type):
                continue
            if not issubclass(asset_class, Asset):
                continue
            if inspect.isabstract(asset_class):
                continue
            if asset_class.__domain_class__ is not domain_class:
                continue
            self._childwise_graph[asset_class] = asset_class.__requires__
        self._parentwise_graph = {}
        for child, parent in self._childwise_graph.items():
            if parent not in self._parentwise_graph:
                self._parentwise_graph[parent] = set()
            if child not in self._parentwise_graph:
                self._parentwise_graph[child] = set()
            self._parentwise_graph[parent].add(child)

    ### PUBLIC METHODS ###

    def in_order(self):
        ordered_asset_classes = []
        parentwise_graph = copy.copy(self.parentwise_graph)
        childwise_graph = copy.copy(self.childwise_graph)
        while childwise_graph:
            for child, parent in sorted(
                childwise_graph.items(),
                key=lambda x: x[0].__name__,
                ):
                if parent is not None:
                    continue
                ordered_asset_classes.append(child)
                del(childwise_graph[child])
                for descendant in parentwise_graph[child]:
                    childwise_graph[descendant] = None
        return tuple(ordered_asset_classes)

    ### PUBLIC PROPERTIES ###

    @property
    def childwise_graph(self):
        return self._childwise_graph

    @property
    def parentwise_graph(self):
        return self._parentwise_graph

    @property
    def domain_class(self):
        return self._domain_class