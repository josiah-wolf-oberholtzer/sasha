from __future__ import print_function
import os
import sys
import traceback
from abjad.tools import pitchtools


class Bootstrap(object):

    ### SPECIAL METHODS ###

    def __call__(self):
        self.delete_mongodb_database()
        self.create_mongodb_database()
        self.populate_mongodb_primary()
        self.populate_all_assets()
        self.populate_mongodb_clusters()
        self.populate_mongodb_partials()
        self.populate_mongodb_spectral_descriptors()
        self.delete_audiodb_databases()
        self.create_audiodb_databases()
        self.populate_audiodb_databases()

    ### PRIVATE METHODS ###

    @staticmethod
    def _collect_instrument_parents(fixtures):
        mapping = {}
        for fixture in fixtures:
            child_name = fixture['name']
            parent_name = fixture['parent']
            if parent_name is None:
                mapping[child_name] = []
                continue
            parents = [parent_name] + mapping[parent_name]
            mapping[child_name] = parents
        return mapping

    @staticmethod
    def _populate_all_assets_for_event(event, event_index, event_total):
        from sasha.tools.assettools import AssetDependencyGraph
        dependency_graph = AssetDependencyGraph()
        asset_classes = dependency_graph.in_order()
        message = 'Populating assets for {} of {}: {}'.format(
            event_index,
            event_total,
            event.name,
            )
        print(message)
        asset_classes = tuple(_ for _ in asset_classes if hasattr(_, 'write'))
        for asset_index, asset_class in enumerate(asset_classes, 1):
            asset = asset_class(event)
            try:
                message = '\t[{}/{}: {}/{}] {}'
                message = message.format(
                    event_index,
                    event_total,
                    asset_index,
                    len(asset_classes),
                    asset,
                    )
                print(message)
                message = '\t\tWriting to {}.'.format(
                    os.path.relpath(asset.path))
                print(message)
                asset.write(parallel=False)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                traceback.print_exc()
                message = 'Writing {} failed.'.format(asset)
                print(message)

    @staticmethod
    def _sort_instrument_fixtures(fixtures):
        fixture_mapping = {}
        childwise_graph = {}
        parentwise_graph = {}
        for fixture in fixtures:
            child_name = fixture['name']
            parent_name = fixture.get('parent', None)
            fixture_mapping[child_name] = fixture
            childwise_graph[child_name] = parent_name
            if parent_name not in parentwise_graph:
                parentwise_graph[parent_name] = set()
            parentwise_graph[parent_name].add(child_name)
        ordered_fixtures = []
        counter = 0
        while childwise_graph:
            items = sorted(childwise_graph.items())
            for child_name, parent_name in items:
                if parent_name:
                    continue
                ordered_fixtures.append(fixture_mapping[child_name])
                del(childwise_graph[child_name])
                for descendant_name in parentwise_graph.get(child_name, []):
                    childwise_graph[descendant_name] = None
            counter += 1
            if 100 < counter:
                raise Exception
        return tuple(ordered_fixtures)

    ### PUBLIC METHODS ###

    @staticmethod
    def create_audiodb_databases():
        from sasha import sasha_configuration
        from sasha.tools.executabletools import AudioDB
        for name in sasha_configuration['audioDB']:
            AudioDB(name).create()

    @staticmethod
    def create_mongodb_database():
        pass

    @staticmethod
    def delete_all_assets():
        from sasha.tools import modeltools
        from sasha.tools import assettools
        asset_classes = assettools.AssetDependencyGraph().in_order()
        for event in modeltools.Event.objects:
            for asset_class in asset_classes:
                if hasattr(asset_class, 'delete'):
                    asset_class(event).delete()

    @staticmethod
    def delete_audiodb_databases():
        from sasha import sasha_configuration
        from sasha.tools.executabletools import AudioDB
        for name in sasha_configuration['audioDB']:
            AudioDB(name).delete()

    @staticmethod
    def delete_mongodb_database():
        from sasha import sasha_configuration
        client = sasha_configuration.mongodb_client
        if client is not None:
            client.drop_database(sasha_configuration.mongodb_database_name)

    @staticmethod
    def populate_all_assets():
        from sasha.tools import modeltools
        events = modeltools.Event.objects
        event_count = events.count()
        message = 'Populating all assets for {} events.'.format(event_count)
        print(message)
        events = tuple(events)
        for event_index, event in enumerate(events, 1):
            Bootstrap._populate_all_assets_for_event(
                event,
                event_index,
                event_count,
                )

    @staticmethod
    def populate_audiodb_databases():
        from sasha import sasha_configuration
        from sasha.tools.executabletools import AudioDB
        from sasha.tools.modeltools import Event
        events = tuple(Event.objects)
        assert 0 < len(events)
        for name in sasha_configuration['audioDB']:
            adb = AudioDB(name)
            adb.populate(events)

    @staticmethod
    def populate_mongodb_primary():
        from sasha import sasha_configuration
        from sasha.tools import assettools
        from sasha.tools import modeltools
        # Populate performers.
        performer_fixtures = sasha_configuration.get_fixtures(
            modeltools.Performer)
        performers = []
        for fixture in performer_fixtures:
            performer = modeltools.Performer(
                name=fixture['name'],
                )
            performers.append(performer)
        assert performers
        modeltools.Performer.objects.insert(performers)
        # Populate instruments.
        instrument_fixtures = sasha_configuration.get_fixtures(
            modeltools.Instrument)
        instrument_fixtures = Bootstrap._sort_instrument_fixtures(
            instrument_fixtures)
        instruments = []
        for fixture in instrument_fixtures:
            instrument = modeltools.Instrument(
                key_names=fixture['key_names'],
                name=fixture['name'],
                transposition=int(fixture['transposition']),
                )
            instruments.append(instrument)
        assert instruments
        modeltools.Instrument.objects.insert(instruments)
        instrument_mapping = Bootstrap._collect_instrument_parents(
            instrument_fixtures)
        for child_name, parent_names in instrument_mapping.items():
            if not parent_names:
                continue
            child = modeltools.Instrument.objects(name=child_name).first()
            parents = []
            for parent_name in parent_names:
                parent = modeltools.Instrument.objects(
                    name=parent_name).first()
                parents.append(parent)
            child.parents = parents
            child.save()
        # Populate events.
        event_fixtures = sasha_configuration.get_fixtures(
            modeltools.Event)
        events = []
        for fixture in event_fixtures:
            instrument = modeltools.Instrument.objects(
                name=fixture['instrument'],
                ).first()
            performer = modeltools.Performer.objects(
                name=fixture['performer'],
                ).first()
            fingering = modeltools.Fingering(
                instrument=instrument,
                key_names=fixture['fingering'],
                )
            fingering.compact_representation = \
                modeltools.Fingering.get_compact_representation(
                    fingering.key_names,
                    instrument.key_names,
                    )
            event = modeltools.Event(
                fingering=fingering,
                name=fixture['name'],
                performer=performer,
                )
            event.md5 = assettools.SourceAudio(event).md5
            events.append(event)
        assert events
        modeltools.Event.objects.insert(events)

    @staticmethod
    def populate_mongodb_clusters():
        from sasha.tools import analysistools
        from sasha.tools import modeltools
        chroma_kmeans = analysistools.KMeansClustering(
            feature='chroma',
            cluster_count=9,
            use_pca=False,
            )
        constant_q_kmeans = analysistools.KMeansClustering(
            feature='constant_q',
            cluster_count=9,
            use_pca=False,
            )
        mfcc_kmeans = analysistools.KMeansClustering(
            feature='mfcc',
            cluster_count=9,
            use_pca=False,
            )
        all_clusters = []
        all_clusters.extend(chroma_kmeans())
        all_clusters.extend(constant_q_kmeans())
        all_clusters.extend(mfcc_kmeans())
        modeltools.Cluster.objects.insert(all_clusters)
        for cluster in modeltools.Cluster.objects:
            for event in cluster.events:
                event.clusters.append(cluster)
                event.save()

    @staticmethod
    def populate_mongodb_partials():
        from sasha.tools import assettools
        from sasha.tools import modeltools
        for event in modeltools.Event.objects:
            chord = assettools.ChordAnalysis(event.name).read()
            partials = []
            for pitch_number, amplitude in chord:
                pitch = pitchtools.NamedPitch(pitch_number)
                pitch_class_number = pitch.pitch_class_number
                octave_number = pitch.octave_number
                partial = modeltools.Partial(
                    amplitude=amplitude,
                    octave_number=octave_number,
                    pitch_class_number=pitch_class_number,
                    pitch_number=pitch_number,
                    )
                partials.append(partial)
            event.partials = partials
            event.save()

    @staticmethod
    def populate_mongodb_spectral_descriptors():
        from sasha.tools import modeltools
        for event in modeltools.Event.objects:
            descriptors = modeltools.Descriptors.from_event(event)
            event.descriptors = descriptors
            event.save()

    @staticmethod
    def rebuild_mongodb_database():
        Bootstrap.delete_mongodb_database()
        Bootstrap.create_mongodb_database()
        Bootstrap.populate_mongodb_primary()
        Bootstrap.populate_mongodb_clusters()
        Bootstrap.populate_mongodb_partials()
        Bootstrap.populate_mongodb_spectral_descriptors()

    @staticmethod
    def rebuild_audiodb_databases():
        Bootstrap.delete_audiodb_databases()
        Bootstrap.create_audiodb_databases()
        Bootstrap.populate_audiodb_databases()