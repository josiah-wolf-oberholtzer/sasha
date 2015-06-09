from sasha.tools import assettools
from sasha.tools import domaintools


def test_AssetDependencyGraph_01():
    domain_class = domaintools.Event
    graph = assettools.AssetDependencyGraph(domain_class)
    asset_classes = graph.in_order()
    assert asset_classes == (
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
        assettools.ChordNotation,
        assettools.ChromaNotation,
        )


def test_AssetDependencyGraph_02():
    domain_class = domaintools.Fingering
    graph = assettools.AssetDependencyGraph(domain_class)
    asset_classes = graph.in_order()
    assert asset_classes == (
        assettools.FingeringNotation,
        )