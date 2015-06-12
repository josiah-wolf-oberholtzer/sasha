from sasha.tools.assettools.PartialTrackingAnalysis import PartialTrackingAnalysis
from sasha.tools.assettools.Plot import Plot


class PartialTrackingPlot(Plot):

    ### CLASS VARIABLES ###

    __requires__ = PartialTrackingAnalysis
    __slots__ = ()
    plugin_label = 'partials'

    ### PRIVATE METHODS ###

    def _build_plot(self):
        from sasha.tools import analysistools
        pta = PartialTrackingAnalysis(self)
        assert pta.exists
        partials = pta.read()
        assert len(partials)
        figure = analysistools.PartialTracker().plot(partials)
        return figure