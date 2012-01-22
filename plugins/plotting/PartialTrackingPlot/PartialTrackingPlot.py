from sasha.plugins.analysis import PartialTrackingAnalysis
from sasha.plugins.plotting._Plot import _Plot
from sasha.tools.analysistools import PartialTracker


class PartialTrackingPlot(_Plot):

    __requires__ = PartialTrackingAnalysis

    plugin_label = 'partials'

    def _build_plot(self):
        pta = PartialTrackingAnalysis(self)
        assert pta.exists
        partials = pta.read( )
        assert len(partials)
        figure = PartialTracker( ).plot(partials)
        return figure

