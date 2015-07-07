import mongoengine


class Fingering(mongoengine.EmbeddedDocument):

    ### MONGOENGINE ###

    instrument = mongoengine.ReferenceField('Instrument')
    key_names = mongoengine.ListField(mongoengine.StringField(max_length=5))