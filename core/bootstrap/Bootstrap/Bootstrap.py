from sasha.core.bootstrap._create_audiodb_databases import _create_audiodb_databases
from sasha.core.bootstrap._create_media_assets import _create_media_assets
from sasha.core.bootstrap._create_media_assets_for_event import _create_media_assets_for_event
from sasha.core.bootstrap._create_sqlite3_database import _create_sqlite3_database
from sasha.core.bootstrap._populate_audiodb_databases import _populate_audiodb_databases
from sasha.core.bootstrap._populate_sqlite3_database import _populate_sqlite3_database
from sasha.core.bootstrap._delete_audiodb_databases import _delete_audiodb_databases
from sasha.core.bootstrap._delete_media_assets import _delete_media_assets
from sasha.core.bootstrap._delete_sqlite3_database import _delete_sqlite3_database
from sasha.core.bootstrap._verify_event_fixtures import _verify_event_fixtures
from sasha.core.bootstrap._verify_instrument_fixtures import _verify_instrument_fixtures
from sasha.core.bootstrap._verify_performer_fixtures import _verify_performer_fixtures
from sasha.core.bootstrap._verify_source_material_integrity import _verify_source_material_integrity


class Bootstrap(object):

    def __call__(self):
        self.verify_source_materials( )

        self.delete_sqlite3_database( )
        self.delete_audiodb_databases( )

        self.create_sqlite3_database( )
        self.create_media_assets( )
        self.create_audiodb_databases( )

    ### PUBLIC METHODS ###

    def create_audiodb_databases(self):
        _create_audiodb_databases( )
        _populate_audiodb_databases( )

    def create_media_assets(self, klasses = [ ]):
        _create_media_assets(klasses)

    def create_sqlite3_database(self):
        _create_sqlite3_database( )
        _populate_sqlite3_database( )

    def delete_audiodb_databases(self):
        _delete_audiodb_databases( )

    def delete_media_assets(self):
        _delete_media_assets( )

    def delete_sqlite3_database(self):
        _delete_sqlite3_database( )

    def verify_source_materials(self):
        _verify_event_fixtures( )
        _verify_instrument_fixtures( )
        _verify_performer_fixtures( )
        _verify_source_material_integrity( )
