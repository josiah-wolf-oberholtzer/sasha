import mongoengine


class Fingering(mongoengine.EmbeddedDocument):

    ### MONGOENGINE ###

    compact_representation = mongoengine.StringField(max_length=50)
    instrument = mongoengine.ReferenceField('Instrument')
    key_names = mongoengine.ListField(mongoengine.StringField(max_length=5))

    ### PUBLIC METHODS ###

    def generate_compact_representation(self):
        result = ''
        for key in sorted(self.instrument.key_names):
            if key in self.key_names:
                result += '1'
            else:
                result += '0'
        return result
