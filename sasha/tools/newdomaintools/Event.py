import mongoengine


class Event(mongoengine.Document):

    ### MONGOENGINE ###

    description = mongoengine.StringField()
    fingering = mongoengine.ListField(
        mongoengine.StringField(max_length=5),
        )
    instrument = mongoengine.ReferenceField('Instrument')
    md5 = mongoengine.StringField(max_length=32)
    name = mongoengine.StringField(max_length=100)
    performer = mongoengine.ReferenceField('Performer')
    partials = mongoengine.EmbeddedDocumentListField('Partial')

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
                'instrument',
                'fingering',
                'partials',
                ],
            )

    ### PUBLIC METHODS ###

    def query_audiodb(self, method, limit=10):
        from sasha.tools import domaintools
        from sasha.tools import executabletools
        adb = executabletools.AudioDB(method)
        event = domaintools.Event.get_one(name=self.name)
        return adb.query(event, limit)

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
        from sasha.tools import newdomaintools
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
            instrument = newdomaintools.Instrument.objects(
                name=instrument_name,
                ).first()
            query['instrument'] = instrument
        if with_keys:
            query['fingering__all'] = with_keys
        if without_keys:
            query['fingering__nin'] = without_keys
        if with_pitches:
            query['partials__pitch_number__all'] = with_pitches
        if without_pitches:
            query['partials__pitch_number__nin'] = without_pitches
        if with_pitch_classes:
            query['partials__pitch_class_number__all'] = with_pitch_classes
        if without_pitch_classes:
            query['partials__pitch_class_number__nin'] = without_pitch_classes
        query = newdomaintools.Event.objects(**query)
        return query

    ### PUBLIC PROPERTIES ###

    @property
    def clusters(self):
        from sasha.tools import newdomaintools
        return newdomaintools.Cluster.objects(events=self)