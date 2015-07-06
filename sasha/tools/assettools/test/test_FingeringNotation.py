import os
from abjad.tools import stringtools
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import domaintools


sasha_configuration.environment = 'testing'


def test_FingeringNotation_01():
    event = domaintools.Event.get_one(id=1)
    plugin = assettools.FingeringNotation(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists


def test_FingeringNotation_02():
    event_a = domaintools.Event.get_one(id=1)
    fingering_a = event_a.fingering._generate_compact_representation()
    instrument_a = stringtools.to_snake_case(event_a.instrument.name)
    event_b = domaintools.Event.get_one(id=2)
    fingering_b = event_b.fingering._generate_compact_representation()
    instrument_b = stringtools.to_snake_case(event_b.instrument.name)
    analysis_a = assettools.FingeringNotation(event_a)
    analysis_b = assettools.FingeringNotation(event_b)
    assert analysis_a.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'fingering__{}__{}__fingering.png'.format(
            instrument_a,
            fingering_a,
            ),
        )
    assert analysis_b.path == os.path.join(
        sasha_configuration.get_media_path('scores'),
        'fingering__{}__{}__fingering.png'.format(
            instrument_b,
            fingering_b,
            ),
        )