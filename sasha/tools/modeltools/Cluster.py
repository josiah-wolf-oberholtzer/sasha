# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from webhelpers.html import HTML
import mongoengine


class Cluster(mongoengine.Document):

    ### MONGOENGINE ###

    cluster_id = mongoengine.IntField(required=True)
    events = mongoengine.ListField(mongoengine.ReferenceField('Event'))
    feature = mongoengine.StringField(required=True)
    technique = mongoengine.StringField(required=True)

    ### PUBLIC METHODS ###

    def get_long_link(self, request):
        href = self.get_url(request)
        text = self.long_link_text.decode('utf-8')
        return HTML.tag('a', href=href, c=text)

    def get_short_link(self, request):
        href = self.get_url(request)
        text = self.short_link_text.decode('utf-8')
        return HTML.tag('a', href=href, c=text)

    def get_url(self, request):
        return request.route_url(
            'cluster',
            feature=self.dash_case_feature,
            cluster_id=self.cluster_id,
            _app_url='',
            )

    ### PUBLIC PROPERTIES ###

    @property
    def dash_case_feature(self):
        return stringtools.to_dash_case(self.feature)

    @property
    def long_link_text(self):
        text = '{} № {}'.format(
            self.title_case_feature,
            self.cluster_id,
            )
        return text

    @property
    def short_link_text(self):
        text = '№ {}'.format(
            self.cluster_id,
            )
        return text

    @property
    def title_case_feature(self):
        if self.feature == 'mfcc':
            return 'MFCC'
        elif self.feature == 'constant_q':
            return 'Constant-Q'
        elif self.feature == 'chroma':
            return 'Chroma'
        raise ValueError