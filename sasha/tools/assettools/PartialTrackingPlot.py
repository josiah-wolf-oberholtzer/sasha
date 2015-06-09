from sasha.tools import analysistools
from sasha.tools.assettools.PartialTrackingAnalysis import PartialTrackingAnalysis
from sasha.tools.assettools.Plot import Plot


class PartialTrackingPlot(Plot):

    __requires__ = PartialTrackingAnalysis

    plugin_label = 'partials'

    def _build_plot(self):
        pta = PartialTrackingAnalysis(self)
        assert pta.exists
        partials = pta.read()
        assert len(partials)
        figure = analysistools.PartialTracker().plot(partials)
        return figure
