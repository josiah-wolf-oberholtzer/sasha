import mongoengine


class Partial(mongoengine.EmbeddedDocument):

    ### MONGOENGINE ###

    amplitude = mongoengine.FloatField()
    octave_number = mongoengine.FloatField()
    pitch_class_number = mongoengine.FloatField()
    pitch_number = mongoengine.FloatField()

    ### SPECIAL METHODS ###

    def __repr__(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatManager.get_repr_format(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _repr_specification(self):
        from abjad.tools.topleveltools import new
        return new(
            self._storage_format_specification,
            is_indented=False,
            )

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            keyword_argument_names=[
                'amplitude',
                'octave_number',
                'pitch_class_number',
                'pitch_number',
                ],
            )
