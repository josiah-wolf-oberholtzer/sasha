import mongoengine


class Partial(mongoengine.EmbeddedDocument):

    ### MONGOENGINE ###

    amplitude = mongoengine.FloatField()
    octave_number = mongoengine.FloatField()
    pitch_class_number = mongoengine.FloatField()
    pitch_number = mongoengine.FloatField()