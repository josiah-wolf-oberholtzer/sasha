import mongoengine


class Instrument(mongoengine.Document):

    ### MONGOENGINE ###

    description = mongoengine.StringField()
    key_names = mongoengine.ListField(mongoengine.StringField(max_length=5))
    name = mongoengine.StringField(required=True, max_length=50)
    parents = mongoengine.ListField(mongoengine.ReferenceField('Instrument'))
    transposition = mongoengine.IntField(default=0)

    ### PUBLIC METHODS ###

    @classmethod
    def with_events(cls):
        from sasha.tools import newdomaintools
        return newdomaintools.Event.objects.only('instrument').distinct()

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        return set(type(self).objects(parents=self))