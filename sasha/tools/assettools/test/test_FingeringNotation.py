import os
from abjad.tools import stringtools
from sasha import sasha_configuration
from sasha.tools import assettools
from sasha.tools import newdomaintools


sasha_configuration.environment = 'testing'


def test_FingeringNotation_01():
    event = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    plugin = assettools.FingeringNotation(event)
    plugin.delete()
    assert not plugin.exists
    plugin.write()
    assert plugin.exists


def test_FingeringNotation_02():
    event_a = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_042.aif')
    fingering_a = event_a.fingering.get_compact_representation(
        event_a.fingering.key_names,
        event_a.fingering.instrument.key_names,
        )
    instrument_a = stringtools.to_snake_case(event_a.fingering.instrument.name)
    event_b = newdomaintools.Event.objects.get(name='event__alto_saxophone__br_123.aif')
    fingering_b = event_b.fingering.get_compact_representation(
        event_b.fingering.key_names,
        event_b.fingering.instrument.key_names,
        )
    instrument_b = stringtools.to_snake_case(event_b.fingering.instrument.name)
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