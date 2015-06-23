import mongoengine


class Performer(mongoengine.Document):

    ### MONGOENGINE ###

    description = mongoengine.StringField()
    name = mongoengine.StringField(required=True, max_length=50)