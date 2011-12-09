import os
from sasha import SASHACFG
from sasha.core.exceptions import UnmatchedSourceMaterialError


def _verify_source_material_integrity( ):

    print 'VERIFYING SOURCE MATERIAL INTEGRITY:',

    fixture_path = os.path.join(SASHACFG.get_media_path('fixtures'), 'events')
    fixture_filenames = filter(lambda x: x.endswith('.fixture'), os.listdir(fixture_path))

    audio_path = SASHACFG.get_media_path('source_audio')
    audio_filenames = filter(lambda x: not x.startswith('.'), os.listdir(audio_path))

    unmatched_fixtures = [ ]
    unmatched_audio = [ ]

    for filename in fixture_filenames:
        if filename.partition('.fixture')[0] not in audio_filenames:
            unmatched_fixtures.append(filename)

    for filename in audio_filenames:
        if '%s.fixture' % filename not in fixture_filenames:
            unmatched_audio.append(filename)

    errors = ''

    if unmatched_fixtures:
        errors += '\nIn %s:\n\t%s' % (fixture_path, '\n\t'.join(unmatched_fixtures))

    if unmatched_audio:
        errors += '\nIn %s:\n\t%s' % (audio_path, '\n\t'.join(unmatched_audio))
        
    if errors:
        raise UnmatchedSourceMaterialError(errors)

    print '...ok!'
