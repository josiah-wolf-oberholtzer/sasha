class Bootstrap(object):

    def __call__(self):
        self.populate_sqlite_primary( )
        self.populate_assets( )
        self.populate_audiodb( )
        self.populate_sqlite_secondary( )

    def create_audiodb_databases(self):
        pass

    def create_sqlite_database(self):
        pass

    def delete_all_assets(self):
        pass

    def delete_audiodb_databases(self):
        pass

    def delete_sqlite_database(self):
        pass

    def populate_all_assets(self):
        pass

    def populate_audiodb_databases(self):
        pass

    def populate_sqlite_primary(self):
        pass

    def populate_sqlite_secondary(self):
        pass
