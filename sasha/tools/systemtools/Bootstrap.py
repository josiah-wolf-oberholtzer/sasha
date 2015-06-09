import multiprocessing
import os
import sys
import traceback
from abjad.tools import pitchtools
from sqlalchemy import create_engine


class Bootstrap(object):

    def __call__(self):
        from sasha import sasha_configuration
        sasha_configuration.logger.info('BOOTSTRAP: Start')
        self.delete_sqlite_database()
        self.delete_audiodb_databases()
        # self.delete_all_assets()
        self.create_sqlite_database()
        self.populate_sqlite_primary()
        self.populate_all_assets()
        self.create_audiodb_databases()
        self.populate_audiodb_databases()
        self.populate_sqlite_secondary()
        sasha_configuration.logger.info('BOOTSTRAP: Stop')

    ### PRIVATE METHODS ###

    @staticmethod
    def _populate_all_assets_for_object(args):
        from sasha import sasha_configuration
        domain_class, object_id, plugin_classes = args
        obj = domain_class.get_one(id=object_id)
        for plugin_class in plugin_classes:
            plugin = plugin_class(obj)
            try:
                if hasattr(plugin, 'write'):
                    sasha_configuration.logger.info('Writing %s.' % plugin)
                    plugin.write(parallel=False)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                exc = traceback.print_exc()
                sasha_configuration.logger.warning('Writing %s failed.' % plugin)
                if exc:
                    sasha_configuration.logger.warning('\n' + exc)

    ### PUBLIC METHODS ###

    def create_audiodb_databases(self):
        from sasha import sasha_configuration
        from sasha.tools.wrappertools import AudioDB
        sasha_configuration.logger.info('Creating audioDB databases.')
        for name in sasha_configuration['audioDB']:
            AudioDB(name).create()

    def create_sqlite_database(self):
        from sasha import sasha_configuration
        from sasha.tools.domaintools import Event
        sasha_configuration.logger.info('Creating empty SQLite database.')
        dbpath = os.path.join(
            sasha_configuration.get_media_path('databases'),
            sasha_configuration['sqlite']['sqlite'],
            )
        engine = create_engine('sqlite:///%s' % dbpath)
        metadata = Event.metadata
        metadata.drop_all(engine)
        metadata.create_all(engine)

    def delete_all_assets(self):
        from sasha import sasha_configuration
        from sasha.tools.assettools import PluginGraph
        sasha_configuration.logger.info('Deleting all assets.')
        for klass in sasha_configuration.get_domain_classes():
            plugins = PluginGraph(klass).in_order()
            for instance in klass.get():
                for plugin in plugins:
                    if hasattr(plugin, 'delete'):
                        plugin(instance).delete()

    def delete_audiodb_databases(self):
        from sasha import sasha_configuration
        from sasha.tools.wrappertools import AudioDB
        sasha_configuration.logger.info('Deleting audioDB databases.')
        for name in sasha_configuration['audioDB']:
            AudioDB(name).delete()

    def delete_sqlite_database(self):
        from sasha import sasha_configuration
        sasha_configuration.logger.info('Deleting sqlite database.')
        path = os.path.join(sasha_configuration.get_media_path('databases'),
            sasha_configuration['sqlite']['sqlite'])
        if os.path.exists(path):
            os.remove(path)

    def populate_all_assets(self):
        from sasha import sasha_configuration
        from sasha.tools.assettools import PluginGraph
        sasha_configuration.logger.info('Populating all assets.')
        for domain_class in sasha_configuration.get_domain_classes():
            log_message = 'Populating plugins for %s.' % domain_class.__name__
            sasha_configuration.logger.info(log_message)
            plugins = PluginGraph(domain_class).in_order()
            triples = [
                (domain_class, x.id, plugins)
                for x in domain_class.get()
                ]
            if triples:
                if 1 < multiprocessing.cpu_count():
                    pool = multiprocessing.Pool()
                    pool.map_async(
                        self._populate_all_assets_for_object,
                        triples,
                        )
                    pool.close()
                    pool.join()
                else:
                    for triple in triples:
                        self._populate_all_assets_for_object(triple)

    def populate_audiodb_databases(self):
        from sasha import sasha_configuration
        from sasha.tools.wrappertools import AudioDB
        from sasha.tools.domaintools import Event
        sasha_configuration.logger.info('Populating audioDB databases.')
        events = Event.get()
        assert 0 < len(events)
        for name in sasha_configuration['audioDB']:
            adb = AudioDB(name)
            adb.populate(events)

    def populate_sqlite_primary(self):
        from sasha import sasha_configuration
        from sasha.tools.domaintools import Event
        from sasha.tools.domaintools import Fingering
        from sasha.tools.domaintools import Instrument
        from sasha.tools.domaintools import InstrumentKey
        from sasha.tools.domaintools import Performer
        from sasha.tools.assettools import SourceAudio
        sasha_configuration.logger.info('Populating SQLite primary objects.')
        session = sasha_configuration.get_session()
        # PERFORMERS
        for fixture in Performer.get_fixtures():
            data = fixture['main']
            session.add(Performer(name=data['name'],
                description=data['description']))
        session.commit()
        # INSTRUMENTS, KEYS
        for fixture in Instrument.get_fixtures():
            data = fixture['main']
            instrument = Instrument(name=data['name'], transposition=int(data['transposition']))
            session.add(instrument)
            session.commit()
            instrument_keys = filter(None, data['instrument_keys.name'].split(' '))
            for instrument_key in instrument_keys:
                session.add(InstrumentKey(name=instrument_key, instrument=instrument))
                session.commit()
        for fixture in Instrument.get_fixtures():
            data = fixture['main']
            if data['parent.name']:
                child = session.query(Instrument).filter_by(name=data['name']).one()
                parent = session.query(Instrument).filter_by(name=data['parent.name']).one()
                child.parent = parent
            session.commit()
        # EVENTS, FINGERINGS
        for fixture in Event.get_fixtures():
            data = fixture['main']
            instrument = session.query(Instrument).filter_by(name=data['instrument.name']).one()
            name = data['name']
            performer = session.query(Performer).filter_by(name=data['performer.name']).one()
            fingering = Fingering(instrument=instrument)
            key_names = filter(None, data['fingering.instrument_keys.name'].split(' '))
            if key_names:
                instrument_keys = session.query(InstrumentKey).filter(
                    InstrumentKey.instrument == instrument).filter(
                    InstrumentKey.name.in_(key_names))
                fingering.instrument_keys.extend(instrument_keys)
            fingering.compact_representation = fingering._generate_compact_representation()
            # check if the fingering already exists
            extant_fingering = Fingering.get(instrument=fingering.instrument,
                compact_representation=fingering.compact_representation)
            if not extant_fingering:
                session.add(fingering)
            else:
                fingering = extant_fingering[0]
            event = Event(fingering=fingering,
                instrument=instrument,
                name=name,
                performer=performer)
            md5 = SourceAudio(event).md5
            event.md5 = md5
            session.add(event)
        session.commit()

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
                session.add(Partial(event_id=event.id,
                    pitch_number=pitch_number,
                    pitch_class_number=pitch_class_number,
                    octave_number=octave_number,
                    amplitude=amplitude))
            session.commit()
        # insert Clusters
        chroma_kmeans = KMeansClustering('chroma', cluster_count=8, use_pca=False)
        constant_q_kmeans = KMeansClustering('constant_q', cluster_count=8, use_pca=False)
        mfcc_kmeans = KMeansClustering('mfcc', cluster_count=8, use_pca=False)
        all_clusters = []
        all_clusters.extend(chroma_kmeans())
        all_clusters.extend(constant_q_kmeans())
        all_clusters.extend(mfcc_kmeans())
        for cluster in all_clusters:
            session.merge(cluster)
        session.commit()

    def rebuild_sqlite_database(self):
        self.delete_sqlite_database()
        self.create_sqlite_database()
        self.populate_sqlite_primary()
        self.populate_sqlite_secondary()