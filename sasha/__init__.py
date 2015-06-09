import os
SASHAROOT = os.path.abspath(os.path.dirname(__file__))
del os

from sasha.tools.systemtools import SashaConfig
SASHA = SashaConfig()
del SashaConfig

from sasha.tools import *
from sasha.tools.domaintools import *
from sasha.tools.wrappertools import AudioDB
from sasha.tools.mediatools import play
del tools