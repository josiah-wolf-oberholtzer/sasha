import os
SASHAROOT = os.path.abspath(os.path.dirname(__file__))
del os

from core.config import SashaConfig
SASHA = SashaConfig( )
del SashaConfig

#from sasha.core.domain import Event
#from sasha.core.domain import Idiom
#from sasha.core.domain import Instrument
#from sasha.core.domain import Performer
from sasha.core.domain import *
from sasha.core.wrappers import AudioDB
del core

