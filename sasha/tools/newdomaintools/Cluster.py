import mongoengine


class Cluster(mongoengine.Document):

    ### MONGOENGINE ###

    cluster_id = mongoengine.IntField(required=True)
    events = mongoengine.ListField(mongoengine.ReferenceField('Event'))
    feature = mongoengine.StringField(required=True)
    technique = mongoengine.StringField(required=True)