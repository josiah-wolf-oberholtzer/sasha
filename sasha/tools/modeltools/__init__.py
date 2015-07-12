from abjad.tools import systemtools

from sasha.tools.modeltools.Descriptors import Descriptors
from sasha.tools.modeltools.Fingering import Fingering

systemtools.ImportManager.import_structured_package(
    __path__[0],
    globals(),
    )

_documentation_section = 'core'