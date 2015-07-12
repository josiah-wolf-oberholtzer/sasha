# -*- encoding: utf-8 -*-
import mongoengine
from webhelpers.html import HTML


class Event(mongoengine.Document):

    ### CLASS VARIABLES ###

    order_by = {
        None: 'md5',
        'spectral_centroid': 'descriptors__spectral_centroid',
        'spectral_crest': 'descriptors__spectral_crest',
        'spectral_flatness': 'descriptors__spectral_flatness',
        'spectral_kurtosis': 'descriptors__spectral_kurtosis',
        'spectral_rolloff': 'descriptors__spectral_rolloff',
        'spectral_skewness': 'descriptors__spectral_skewness',
        'spectral_spread': 'descriptors__spectral_spread',
        }

    ### MONGOENGINE ###

    description = mongoengine.StringField()
    descriptors = mongoengine.EmbeddedDocumentField('Descriptors')
    fingering = mongoengine.EmbeddedDocumentField('Fingering')
    md5 = mongoengine.StringField(max_length=32)
    name = mongoengine.StringField(max_length=100, unique=True)
    performer = mongoengine.ReferenceField('Performer')
    partials = mongoengine.EmbeddedDocumentListField('Partial')

    meta = {
        'ordering': ['-md5'],
        }

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __repr__(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            is_indented=False,
            keyword_argument_names=[
                'name',
                ],
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            keyword_argument_names=[
                'name',
                'fingering',
                'partials',
                ],
            )

    ### PUBLIC METHODS ###

    def get_md5_link(self, request):
        href = self.get_url(request)
        text = self.md5
        return HTML.tag('a', href=href, c=text)

    def get_numbered_link(self, request):
        href = self.get_url(request)
        text = self.link_text.decode('utf-8')
        return HTML.tag('a', href=href, c=text)

    def get_url(self, request):
        return request.route_url('event', md5=self.md5)

    def query_audiodb(self, method, limit=10):
        from sasha.tools import executabletools
        adb = executabletools.AudioDB(method)
        return adb.query(self, limit)

    @staticmethod
    def query_mongodb(
        instrument_name=None,
        with_keys=None,
        without_keys=None,
        with_pitches=None,
        without_pitches=None,
        with_pitch_classes=None,
        without_pitch_classes=None,
        ):
        from sasha.tools import modeltools
        query = {}
        with_keys = with_keys or []
        with_pitch_classes = with_pitch_classes or []
        with_pitches = with_pitches or []
        without_keys = without_keys or []
        without_pitch_classes = without_pitch_classes or []
        without_pitches = without_pitches or []
        if with_keys or without_keys:
            assert instrument_name is not None
        if instrument_name:
            instrument = modeltools.Instrument.objects(
                name=instrument_name,
                ).first()
            query['fingering__instrument'] = instrument
        if with_keys:
            query['fingering__key_names__all'] = with_keys
        if without_keys:
            query['fingering__key_names__nin'] = without_keys
        if with_pitches:
            query['partials__pitch_number__all'] = with_pitches
        if without_pitches:
            query['partials__pitch_number__nin'] = without_pitches
        if with_pitch_classes:
            query['partials__pitch_class_number__all'] = with_pitch_classes
        if without_pitch_classes:
            query['partials__pitch_class_number__nin'] = without_pitch_classes
        query = modeltools.Event.objects(**query)
        return query

    ### PUBLIC PROPERTIES ###

    @property
    def canonical_event_name(self):
        return 'event__{}'.format(self.md5)

    @property
    def canonical_fingering_name(self):
        fingering = self.fingering
        instrument = fingering.instrument
        instrument_name = '_'.join(instrument.name.lower().split())
        return 'fingering__{}__{}'.format(
            instrument_name,
            fingering.compact_representation,
            )

    @property
    def clusters(self):
        from sasha.tools import modeltools
        return modeltools.Cluster.objects(events=self)

    @property
    def link_text(self):
        return 'Event № {}'.format(self.md5[-8:])