from sasha.tools import assettools


def test_AssetDependencyGraph_01():
    graph = assettools.AssetDependencyGraph()
    asset_classes = graph.in_order()
    assert asset_classes == (
        assettools.FingeringNotation,
        assettools.SourceAudio,
        assettools.CroppedAudio,
        assettools.MP3Audio,
        assettools.PartialTrackingAnalysis,
        assettools.ChordAnalysis,
        assettools.ChromaAnalysis,
        assettools.ConstantQAnalysis,
        assettools.LinearSpectrumAnalysis,
        assettools.LogHarmonicityAnalysis,
        assettools.LogPowerAnalysis,
        assettools.MFCCAnalysis,
        assettools.PartialTrackingPlot,
        assettools.ArpeggioNotation,
        assettools.ChordNotation,
        assettools.ChromaNotation,
        )