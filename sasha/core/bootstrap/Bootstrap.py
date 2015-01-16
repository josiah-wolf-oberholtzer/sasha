import logging

from sasha import SASHA
from sasha.core.bootstrap._create_audiodb_databases import _create_audiodb_databases
from sasha.core.bootstrap._create_sqlite_database import _create_sqlite_database
from sasha.core.bootstrap._delete_all_assets import _delete_all_assets
from sasha.core.bootstrap._delete_audiodb_databases import _delete_audiodb_databases
from sasha.core.bootstrap._delete_sqlite_database import _delete_sqlite_database
from sasha.core.bootstrap._populate_all_assets import _populate_all_assets
from sasha.core.bootstrap._populate_audiodb_databases import _populate_audiodb_databases
from sasha.core.bootstrap._populate_sqlite_primary import _populate_sqlite_primary
from sasha.core.bootstrap._populate_sqlite_secondary import _populate_sqlite_secondary


class Bootstrap(object):

    def __call__(self):
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

    ### PUBLIC METHODS ###

    def create_audiodb_databases(self):
        _create_audiodb_databases()        

    def create_sqlite_database(self):
        _create_sqlite_database()

    def delete_all_assets(self):
        _delete_all_assets()

    def delete_audiodb_databases(self):
        _delete_audiodb_databases()

    def delete_sqlite_database(self):
        _delete_sqlite_database()

    def get_fixtures():
        _get_fixtures()

    def populate_all_assets(self):
        _populate_all_assets()

    def populate_audiodb_databases(self):
        _populate_audiodb_databases()

    def populate_sqlite_primary(self):
        _populate_sqlite_primary()

    def populate_sqlite_secondary(self):
        _populate_sqlite_secondary()

    def rebuild_sqlite_database(self):
        _delete_sqlite_database()
        _create_sqlite_database()
        _populate_sqlite_primary()
        _populate_sqlite_secondary()
