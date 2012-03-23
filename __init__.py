import os
SASHAROOT = os.path.abspath(os.path.dirname(__file__))
del os

from sasha.core.config import SashaConfig
SASHA = SashaConfig( )
del SashaConfig

from sasha.core.domain import *
from sasha.core.wrappers import AudioDB
from sasha.tools.mediatools import play

del core
del plugins
del tools

