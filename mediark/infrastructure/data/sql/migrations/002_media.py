class Migration:  # pragma: no cover
    version = '002'

    def __init__(self, context):
        self.context = context
        self.connection = context['connection']
        self.schema = context['schema']
        self.owner = "mediark"
        self._tables = ["media"]

    def schema_up(self):
        database = ""
        for table in self._tables:
            database += self._create_table(table)

        database += "SET enable_seqscan = false;"

        with self.connection.cursor() as cursor:
            cursor.execute(database)

    def _create_table(self, table):
        return (
            f"CREATE TABLE IF NOT EXISTS {self.schema}.{table} (data JSONB);"
            f"ALTER TABLE {self.schema}.{table} OWNER TO {self.owner};"
            f"CREATE UNIQUE INDEX IF NOT EXISTS pk_{table}_id ON "
            f"{self.schema}.{table} ((data ->> 'id'));"
            f"REINDEX INDEX {self.schema}.pk_{table}_id;"
        )

    def schema_down(self):
        """Not implemented."""
