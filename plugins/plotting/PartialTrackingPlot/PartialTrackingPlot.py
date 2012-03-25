from sasha.plugins.analysis import PartialTrackingAnalysis
from sasha.plugins.plotting.Plot import Plot
from sasha.tools.analysistools import PartialTracker


class PartialTrackingPlot(Plot):

    __requires__ = PartialTrackingAnalysis

    plugin_label = 'partials'

    def _build_plot(self):
        pta = PartialTrackingAnalysis(self)
        assert pta.exists
        partials = pta.read( )
        assert len(partials)
        figure = PartialTracker( ).plot(partials)
        return figure

