from pgdb import connect
from typing import Sequence, List, Dict, Any


class SchemaConnection:
    def __init__(self, dsn: str) -> None:
        dsn = dsn.replace('postgresql://', '')
        credentials, location = dsn.split('@')
        user, password = credentials.split(':')
        host, database = location.split('/')
        self.dsn = f'{host}:{database}:{user}:{password}'
        self.connection = None

    def open(self) -> None:
        self.connection = connect(dsn=self.dsn)

    def close(self) -> None:
        if self.connection:
            self.connection.commit()
            self.connection.close()

    def execute(self, statement: str,
                parameters: Sequence[Any] = []) -> str:
        if not self.connection:
            return ''
        cursor = self.connection.cursor()
        cursor.execute(statement, tuple(parameters))
        cursor.close()
        return ''

    def select(self, statement: str,
               parameters: Sequence[Any] = []) -> List[Dict[str, Any]]:
        if not self.connection:
            return []

        cursor = self.connection.cursor()
        cursor.execute(statement, tuple(parameters))
        records = cursor.fetchall()
        cursor.close()
        return [record._asdict() for record in records]
