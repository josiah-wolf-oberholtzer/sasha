from __future__ import print_function
#import multiprocessing
import os
import sys
import traceback
from abjad.tools import pitchtools
from sqlalchemy import create_engine


class Bootstrap(object):

    ### SPECIAL METHODS ###

    def __call__(self):
        from sasha import sasha_configuration
        sasha_configuration.logger.info('BOOTSTRAP: Start')
        self.delete_sqlite_database()
        self.delete_mongodb_database()
        self.delete_audiodb_databases()
        self.create_sqlite_database()
        self.create_mongodb_database()
        self.populate_sqlite_primary()
        self.populate_mongodb_primary()
        self.populate_all_assets()
        self.create_audiodb_databases()
        self.populate_audiodb_databases()
        self.populate_sqlite_secondary()
        self.populate_mongodb_secondary()
        sasha_configuration.logger.info('BOOTSTRAP: Stop')

    ### PRIVATE METHODS ###

    @staticmethod
    def _populate_all_assets_for_object(args):
        from sasha import sasha_configuration
        domain_class, object_id, asset_classes = args
        obj = domain_class.get_one(id=object_id)
        print('Populating assets for {}'.format(obj))
        for asset_class in asset_classes:
            asset = asset_class(obj)
            try:
                if hasattr(asset, 'write'):
                    message = 'Writing {} to {}.'
                    message = message.format(asset, asset.path)
                    print(message)
                    #sasha_configuration.logger.info(message)
                    asset.write(parallel=False)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                exc = traceback.print_exc()
                message = 'Writing {} failed.'.format(asset)
                print(message)
                #sasha_configuration.logger.warning(message)
                if exc:
                    message = '\n' + exc
                    sasha_configuration.logger.warning(message)

    ### PUBLIC METHODS ###

    def create_audiodb_databases(self):
        from sasha import sasha_configuration
        from sasha.tools.executabletools import AudioDB
        sasha_configuration.logger.info('Creating audioDB databases.')
        for name in sasha_configuration['audioDB']:
            AudioDB(name).create()

    def create_mongodb_database(self):
        pass

    def create_sqlite_database(self):
        from sasha import sasha_configuration
        from sasha.tools.domaintools import Event
        sasha_configuration.logger.info('Creating empty SQLite database.')
        database_path = os.path.join(
            sasha_configuration.get_media_path('databases'),
            sasha_configuration['sqlite']['sqlite'],
            )
        database_directory_path, _ = os.path.split(database_path)
        if not os.path.exists(database_directory_path):
            os.makedirs(database_directory_path)
        engine = create_engine('sqlite:///{}'.format(database_path))
        metadata = Event.metadata
        metadata.drop_all(engine)
        metadata.create_all(engine)

    def delete_all_assets(self):
        from sasha import sasha_configuration
        from sasha.tools.assettools import AssetDependencyGraph
        sasha_configuration.logger.info('Deleting all assets.')
        for klass in sasha_configuration.get_domain_classes():
            plugins = AssetDependencyGraph(klass).in_order()
            for instance in klass.get():
                for plugin in plugins:
                    if hasattr(plugin, 'delete'):
                        plugin(instance).delete()

    def delete_audiodb_databases(self):
        from sasha import sasha_configuration
        from sasha.tools.executabletools import AudioDB
        sasha_configuration.logger.info('Deleting audioDB databases.')
        for name in sasha_configuration['audioDB']:
            AudioDB(name).delete()

    def delete_mongodb_database(self):
        from sasha import sasha_configuration
        client = sasha_configuration.mongodb_client
        if client is not None:
            client.drop_database(sasha_configuration.mongodb_database_name)

    def delete_sqlite_database(self):
        from sasha import sasha_configuration
        sasha_configuration.logger.info('Deleting sqlite database.')
        path = os.path.join(sasha_configuration.get_media_path('databases'),
            sasha_configuration['sqlite']['sqlite'])
        if os.path.exists(path):
            os.remove(path)

    def populate_all_assets(self):
        from sasha import sasha_configuration
        from sasha.tools.assettools import AssetDependencyGraph
        sasha_configuration.logger.info('Populating all assets.')
        domain_classes = sasha_configuration.get_domain_classes()
        domain_classes = sorted(domain_classes, key=lambda x: x.__name__)
        for domain_class in domain_classes:
            domain_objects = domain_class.get()
            log_message = 'Populating all {} assets for {} objects.'.format(
                domain_class.__name__,
                len(domain_objects),
                )
            print(log_message)
            sasha_configuration.logger.info(log_message)
            dependency_graph = AssetDependencyGraph(domain_class)
            asset_classes = dependency_graph.in_order()
            if not asset_classes:
                continue
            triples = [
                (domain_class, domain_object.id, asset_classes)
                for domain_object in domain_objects
                ]
            for triple in triples:
                self._populate_all_assets_for_object(triple)
#            if triples:
#                if 1 < multiprocessing.cpu_count():
#                    pool = multiprocessing.Pool()
#                    pool.map_async(
#                        self._populate_all_assets_for_object,
#                        triples,
#                        )
#                    pool.close()
#                    pool.join()
#                else:
#                    for triple in triples:
#                        self._populate_all_assets_for_object(triple)

    def populate_audiodb_databases(self):
        from sasha import sasha_configuration
        from sasha.tools.executabletools import AudioDB
        from sasha.tools.domaintools import Event
        sasha_configuration.logger.info('Populating audioDB databases.')
        events = Event.get()
        assert 0 < len(events)
        for name in sasha_configuration['audioDB']:
            adb = AudioDB(name)
            adb.populate(events)

    def populate_mongodb_primary(self):
        pass

    def populate_sqlite_primary(self):
        from sasha import sasha_configuration
        from sasha.tools import domaintools
        from sasha.tools import assettools
        sasha_configuration.logger.info('Populating SQLite primary objects.')
        session = sasha_configuration.get_session()
        # PERFORMERS
        for fixture in sasha_configuration.get_fixtures(domaintools.Performer):
            performer = domaintools.Performer(
                name=fixture['name'],
                )
            session.add(performer)
        session.commit()
        # INSTRUMENTS, KEYS
        for fixture in sasha_configuration.get_fixtures(domaintools.Instrument):
            instrument = domaintools.Instrument(
                name=fixture['name'],
                transposition=fixture['transposition'],
                )
            session.add(instrument)
            session.commit()
            instrument_keys = fixture['key_names']
            for instrument_key in instrument_keys:
                instrument_key = domaintools.InstrumentKey(
                    name=instrument_key,
                    instrument=instrument,
                    )
                session.add(instrument_key)
                session.commit()
        for fixture in sasha_configuration.get_fixtures(domaintools.Instrument):
            if fixture['parent']:
                child = session.query(domaintools.Instrument).filter_by(
                    name=fixture['name']).one()
                parent = session.query(domaintools.Instrument).filter_by(
                    name=fixture['parent']).one()
                child.parent = parent
            session.commit()
        # EVENTS, FINGERINGS
        for fixture in sasha_configuration.get_fixtures(domaintools.Event):
            instrument = session.query(domaintools.Instrument).filter_by(
                name=fixture['instrument']).one()
            name = fixture['name']
            performer = session.query(domaintools.Performer).filter_by(
                name=fixture['performer']).one()
            fingering = domaintools.Fingering(instrument=instrument)
            key_names = fixture['fingering']
            if key_names:
                instrument_keys = session.query(domaintools.InstrumentKey).filter(
                    domaintools.InstrumentKey.instrument == instrument).filter(
                    domaintools.InstrumentKey.name.in_(key_names))
                fingering.instrument_keys.extend(instrument_keys)
            fingering.compact_representation = \
                fingering._generate_compact_representation()
            # check if the fingering already exists
            extant_fingering = domaintools.Fingering.get(instrument=fingering.instrument,
                compact_representation=fingering.compact_representation)
            if not extant_fingering:
                session.add(fingering)
            else:
                fingering = extant_fingering[0]
            event = domaintools.Event(fingering=fingering,
                instrument=instrument,
                name=name,
                performer=performer)
            md5 = assettools.SourceAudio(event).md5
            event.md5 = md5
            session.add(event)
        session.commit()

    def populate_mongodb_secondary(self):
        pass

    def populate_sqlite_secondary(self):
        from sasha import sasha_configuration
        from sasha.tools.analysistools import KMeansClustering
        from sasha.tools.domaintools import Event
        from sasha.tools.domaintools import Partial
        from sasha.tools.assettools import ChordAnalysis
        sasha_configuration.logger.info('Populate SQLite secondary objects.')
        session = sasha_configuration.get_session()
        # insert Partials
        for event in Event.get():
            chord = ChordAnalysis(event).read()
            for pitch_number, amplitude in chord:
                pitch = pitchtools.NamedPitch(pitch_number)
                pitch_class_number = pitch.pitch_class_number
                octave_number = pitch.octave_number
                partial = Partial(
                    event_id=event.id,
                    pitch_number=pitch_number,
                    pitch_class_number=pitch_class_number,
                    octave_number=octave_number,
                    amplitude=amplitude,
                    )
                session.add(partial)
            session.commit()
        # insert Clusters
        chroma_kmeans = KMeansClustering(
            'chroma',
            cluster_count=9,
            use_pca=False,
            )
        constant_q_kmeans = KMeansClustering(
            'constant_q',
            cluster_count=9,
            use_pca=False,
            )
        mfcc_kmeans = KMeansClustering(
            'mfcc',
            cluster_count=9,
            use_pca=False,
            )
        all_clusters = []
        all_clusters.extend(chroma_kmeans())
        all_clusters.extend(constant_q_kmeans())
        all_clusters.extend(mfcc_kmeans())
        for cluster in all_clusters:
            session.merge(cluster)
        session.commit()

    def rebuild_mongodb_database(self):
        self.delete_mongodb_database()
        self.create_mongodb_database()
        self.populate_mongodb_primary()
        self.populate_mongodb_secondary()

    def rebuild_sqlite_database(self):
        self.delete_sqlite_database()
        self.create_sqlite_database()
        self.populate_sqlite_primary()
        self.populate_sqlite_secondary()