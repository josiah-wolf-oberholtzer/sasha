# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from sasha.tools.domaintools.DomainObject import DomainObject
from sqlalchemy import Column, Integer, String
from webhelpers.html import HTML


class Cluster(DomainObject):

    ### SQLALCHEMY ###

    cluster_id = Column(Integer)
    feature = Column(String(32))
    technique = Column(String(32))

    ### SPECIAL METHODS ###

    def __repr__(self):
        result = '<{}(cluster_id={}, feature={!r})>'
        result = result.format(
            type(self).__name__,
            self.cluster_id,
            self.feature,
            )
        return result

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
