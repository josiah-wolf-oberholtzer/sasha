import mongoengine
from abjad.tools import stringtools
from webhelpers.html import HTML


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

    def find_similar_fingerings(self, n=10):
        def compare(a, b):
            return sum(1 for x, y in zip(a, b) if x == y)
        results = []
        fingerings = Fingering.get(instrument_id=self.instrument_id)
        fingerings = (x for x in fingerings if x.id != self.id)
        for fingering in fingerings:
            comparison = compare(
                self.compact_representation,
                fingering.compact_representation,
                )
            results.append((comparison, fingering))
        results.sort(key=lambda x: x[0], reverse=True)
        results = [x[1] for x in results][:n]
        return results

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

    def get_link(self, request):
        href = self.get_url(request)
        text = self.name
        return HTML.tag('a', href=href, c=text)

    def get_url(self, request):
        instrument_name = self.instrument.dash_case_name
        compact_representation = self.compact_representation
        return request.route_url(
            'fingering',
            instrument_name=instrument_name,
            compact_representation=compact_representation,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        return ' '.join(self.key_names)