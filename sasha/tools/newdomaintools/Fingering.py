import mongoengine


class Fingering(mongoengine.EmbeddedDocument):

    ### MONGOENGINE ###

    compact_representation = mongoengine.StringField(max_length=50)
    instrument = mongoengine.ReferenceField('Instrument')
    key_names = mongoengine.ListField(mongoengine.StringField(max_length=5))

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
                'instrument',
                'key_names',
                ],
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            keyword_argument_names=[
                'instrument',
                'key_names',
                ],
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def get_compact_representation(
        fingering_key_names,
        instrument_key_names,
        ):
        result = ''
        for key in sorted(instrument_key_names):
            if key in fingering_key_names:
                result += '1'
            else:
                result += '0'
        return result