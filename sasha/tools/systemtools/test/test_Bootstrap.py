# -*- encoding: utf-8 -*-
import os
import unittest
from sasha import sasha_configuration
from sasha.tools import executabletools
from sasha.tools import modeltools
from sasha.tools import systemtools


class BootstrapTests(unittest.TestCase):

    def setUp(self):
        sasha_configuration.environment = 'testing'

    def tearDown(self):
        pass

    def test_Bootstrap_create_audiodb_databases_01(self):

        executable = executabletools.AudioDB('chroma').executable
        executable = os.path.abspath(executable)
        print executable, os.path.exists(executable)

        print executabletools.AudioDB('chroma').path
        print executabletools.AudioDB('constant_q').path
        print executabletools.AudioDB('mfcc').path

        #assert executabletools.AudioDB('chroma').exists
        #assert executabletools.AudioDB('constant_q').exists
        #assert executabletools.AudioDB('mfcc').exists

        bootstrap = systemtools.Bootstrap()
        bootstrap.delete_audiodb_databases()
        bootstrap.create_audiodb_databases()

        assert executabletools.AudioDB('chroma').exists
        assert executabletools.AudioDB('constant_q').exists
        assert executabletools.AudioDB('mfcc').exists

    def test_Bootstrap_delete_audiodb_databases_01(self):

        assert executabletools.AudioDB('chroma').exists
        assert executabletools.AudioDB('constant_q').exists
        assert executabletools.AudioDB('mfcc').exists

        bootstrap = systemtools.Bootstrap()
        bootstrap.delete_audiodb_databases()
        assert not executabletools.AudioDB('chroma').exists
        assert not executabletools.AudioDB('constant_q').exists
        assert not executabletools.AudioDB('mfcc').exists
        bootstrap.create_audiodb_databases()

        assert executabletools.AudioDB('chroma').exists
        assert executabletools.AudioDB('constant_q').exists
        assert executabletools.AudioDB('mfcc').exists

    def test_Bootstrap_delete_mongodb_database_01(self):

        bootstrap = systemtools.Bootstrap()
        bootstrap.delete_mongodb_database()

        event_count = modeltools.Event.objects.count()
        instrument_count = modeltools.Instrument.objects.count()
        performer_count = modeltools.Performer.objects.count()

        assert 0 == event_count
        assert 0 == instrument_count
        assert 0 == performer_count

        bootstrap.rebuild_mongodb_database()

    def test_Bootstrap_instruments_01(self):

        bootstrap = systemtools.Bootstrap()
        fixtures = sasha_configuration.get_fixtures(modeltools.Instrument)
        assert fixtures
        fixtures = bootstrap._sort_instrument_fixtures(fixtures)
        assert fixtures
        mapping = bootstrap._collect_instrument_parents(fixtures)
        assert mapping == {
            u'Aerophone': [],
            u'Saxophone': [u'Aerophone'],
            u'Alto Saxophone': [u'Saxophone', u'Aerophone'],
            u'Soprano Saxophone': [u'Saxophone', u'Aerophone'],
            }

    def test_Bootstrap_populate_audiodb_databases_01(self):

        bootstrap = systemtools.Bootstrap()

        event_count = modeltools.Event.objects.count()
        assert 0 < event_count

        assert executabletools.AudioDB('chroma').exists
        assert executabletools.AudioDB('constant_q').exists
        assert executabletools.AudioDB('mfcc').exists

        bootstrap.delete_audiodb_databases()
        bootstrap.create_audiodb_databases()
        bootstrap.populate_audiodb_databases()

        assert executabletools.AudioDB('chroma').exists
        assert executabletools.AudioDB('constant_q').exists
        assert executabletools.AudioDB('mfcc').exists

        adb = executabletools.AudioDB('chroma')
        assert adb.status['num_files'] == event_count

        adb = executabletools.AudioDB('constant_q')
        assert adb.status['num_files'] == event_count

        adb = executabletools.AudioDB('mfcc')
        assert adb.status['num_files'] == event_count

    def test_Bootstrap_populate_mongodb_clusters_01(self):

        bootstrap = systemtools.Bootstrap()
        bootstrap.delete_mongodb_database()
        bootstrap.create_mongodb_database()
        bootstrap.populate_mongodb_primary()
        bootstrap.populate_mongodb_clusters()

        clusters = modeltools.Cluster.objects.all()
        assert clusters

        for cluster in clusters:
            assert len(cluster.events)

        bootstrap.rebuild_mongodb_database()

    def test_Bootstrap_populate_mongodb_partials_01(self):

        bootstrap = systemtools.Bootstrap()
        bootstrap.delete_mongodb_database()
        bootstrap.create_mongodb_database()
        bootstrap.populate_mongodb_primary()
        bootstrap.populate_mongodb_partials()

        for event in modeltools.Event.objects:
            assert event.partials

        bootstrap.rebuild_mongodb_database()

    def test_Bootstrap_populate_mongodb_primary_01(self):

        bootstrap = systemtools.Bootstrap()
        bootstrap.delete_mongodb_database()

        event_count = modeltools.Event.objects.count()
        instrument_count = modeltools.Instrument.objects.count()
        performer_count = modeltools.Performer.objects.count()

        assert 0 == event_count
        assert 0 == instrument_count
        assert 0 == performer_count

        bootstrap.create_mongodb_database()
        bootstrap.populate_mongodb_primary()

        event_count = modeltools.Event.objects.count()
        instrument_count = modeltools.Instrument.objects.count()
        performer_count = modeltools.Performer.objects.count()

        assert 0 < event_count
        assert 0 < instrument_count
        assert 0 < performer_count

        event_fixtures = sasha_configuration.get_fixtures(
            modeltools.Event)
        instrument_fixtures = sasha_configuration.get_fixtures(
            modeltools.Instrument)
        performer_fixtures = sasha_configuration.get_fixtures(
            modeltools.Performer)

        assert len(event_fixtures) == event_count
        assert len(instrument_fixtures) == instrument_count
        assert len(performer_fixtures) == performer_count

        bootstrap.rebuild_mongodb_database()