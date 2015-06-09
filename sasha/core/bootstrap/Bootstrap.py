import multiprocessing
import os
import sys
import traceback
from abjad.tools import pitchtools
from sqlalchemy import create_engine

from sasha import SASHA


class Bootstrap(object):

    def __call__(self):
        from sasha import SASHA
        SASHA.logger.info('BOOTSTRAP: Start')
        self.delete_sqlite_database()
        self.delete_audiodb_databases()
        # self.delete_all_assets()
        self.create_sqlite_database()
        self.populate_sqlite_primary()
        self.populate_all_assets()
        self.create_audiodb_databases()
        self.populate_audiodb_databases()
        self.populate_sqlite_secondary()
        SASHA.logger.info('BOOTSTRAP: Stop')

    ### PRIVATE METHODS ###

    @staticmethod
    def _populate_all_assets_for_object(args):
        domain_class, object_id, plugin_classes = args
        obj = domain_class.get_one(id=object_id)
        for plugin_class in plugin_classes:
            plugin = plugin_class(obj)
            try:
                if hasattr(plugin, 'write'):
                    SASHA.logger.info('Writing %s.' % plugin)
                    plugin.write(parallel=False)
            except:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                exc = traceback.print_exc()
                SASHA.logger.warning('Writing %s failed.' % plugin)
                if exc:
                    SASHA.logger.warning('\n' + exc)

    ### PUBLIC METHODS ###

    def create_audiodb_databases(self):
        from sasha.core.wrappers import AudioDB
        SASHA.logger.info('Creating audioDB databases.')
        for name in SASHA['audioDB']:
            AudioDB(name).create()

    def create_sqlite_database(self):
        from sasha.core.domain import Event
        SASHA.logger.info('Creating empty SQLite database.')
        dbpath = os.path.join(
            SASHA.get_media_path('databases'),
            SASHA['sqlite']['sqlite'],
            )
        engine = create_engine('sqlite:///%s' % dbpath)
        metadata = Event.metadata
        metadata.drop_all(engine)
        metadata.create_all(engine)

    def delete_all_assets(self):
        from sasha.core.plugins import PluginGraph
        SASHA.logger.info('Deleting all assets.')
        for klass in SASHA.get_domain_classes():
            plugins = PluginGraph(klass).in_order()
            for instance in klass.get():
                for plugin in plugins:
                    if hasattr(plugin, 'delete'):
                        plugin(instance).delete()

    def delete_audiodb_databases(self):
        from sasha.core.wrappers import AudioDB
        SASHA.logger.info('Deleting audioDB databases.')
        for name in SASHA['audioDB']:
            AudioDB(name).delete()

    def delete_sqlite_database(self):
        SASHA.logger.info('Deleting sqlite database.')
        path = os.path.join(SASHA.get_media_path('databases'),
            SASHA['sqlite']['sqlite'])
        if os.path.exists(path):
            os.remove(path)

    def populate_all_assets(self):
        from sasha.core.plugins import PluginGraph
        SASHA.logger.info('Populating all assets.')
        for domain_class in SASHA.get_domain_classes():
            SASHA.logger.info('Populating plugins for %s.' % domain_class.__name__)
            plugins = PluginGraph(domain_class).in_order()
            args = [(domain_class, x.id, plugins) for x in domain_class.get()]
            if args:
                if 1 < multiprocessing.cpu_count():
                    pool = multiprocessing.Pool()
                    pool.map_async(self._populate_all_assets_for_object, args)
                    pool.close()
                    pool.join()
                else:
                    map(self._populate_all_assets_for_object, args)

    def populate_audiodb_databases(self):
        from sasha.core.wrappers import AudioDB
        from sasha.core.domain import Event
        SASHA.logger.info('Populating audioDB databases.')
        events = Event.get()
        assert 0 < len(events)
        for name in SASHA['audioDB']:
            adb = AudioDB(name)
            adb.populate(events)

    def populate_sqlite_primary(self):
        from sasha.core.domain import Event
        from sasha.core.domain import Fingering
        from sasha.core.domain import Instrument
        from sasha.core.domain import InstrumentKey
        from sasha.core.domain import Performer
        from sasha.plugins.audio import SourceAudio
        SASHA.logger.info('Populating SQLite primary objects.')
        session = SASHA.get_session()
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
        from sasha.tools.analysistools import KMeansClustering
        from sasha.core.domain import Event
        from sasha.core.domain import Partial
        from sasha.plugins.analysis import ChordAnalysis
        SASHA.logger.info('Populate SQLite secondary objects.')
        session = SASHA.get_session()
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