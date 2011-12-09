import multiprocessing
import sys
import traceback
from sasha.core.domain import Event
from sasha.plugins import *


def _create_media_assets_for_event(args):

    event = args[0]
    klasses = args[1]

    assert isinstance(event, Event)

    logger = multiprocessing.get_logger( )

    assets = [
        ChromaAnalysis,
        ConstantQAnalysis,
        LinearSpectrumAnalysis,
        LogHarmonicityAnalysis,
        LogPowerAnalysis,
        MFCCAnalysis,
        PartialTrackingAnalysis,
        ChordAnalysis,
        MP3Audio,
        ChordNotation,
        ChromaNotation,
#        IdiomNotation,
    ]

    if klasses:
        assets = klasses

    for asset in assets:
        logger.info('WRITING [%04d]: %s' % (event.ID, asset.__name__))
        try:
            asset(event).write(parallel = False)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.warning('\n' + traceback.print_exc())
