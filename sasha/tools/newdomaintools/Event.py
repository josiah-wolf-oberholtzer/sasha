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

    ### PUBLIC PROPERTIES ###

    @property
    def clusters(self):
        from sasha.tools import newdomaintools
        return newdomaintools.Cluster.objects(events=self)