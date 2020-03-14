import logging
import time
import rapidjson as json
from uuid import uuid4
from typing import Dict, List, Generic, Optional, Callable, Any, Union
from asyncpg import Connection
from filtrark.sql_parser import SqlParser
from ....application.models import T
from ....application.repositories import Repository
from ....application.utilities import (
    QueryDomain, TenantProvider, AuthProvider, EntityNotFoundError)
from .connection import ConnectionManager


class SqlRepository(Repository, Generic[T]):
    def __init__(self,
                 table: str,
                 constructor: Callable,
                 tenant_provider: TenantProvider,
                 auth_provider: AuthProvider,
                 connection_manager: ConnectionManager,
                 parser: SqlParser) -> None:
        self.table = table
        self.constructor = constructor
        self.tenant_provider = tenant_provider
        self.auth_provider = auth_provider
        self.connection_manager = connection_manager
        self.parser = parser
        self.max_items = 1000

    async def add(self, item: Union[T, List[T]]) -> List[T]:
        tenant = self.tenant_provider.tenant
        user = self.auth_provider.user

        records = []
        items = item if isinstance(item, list) else [item]
        for item in items:
            item.id = item.id or str(uuid4())
            item.updated_at = int(time.time())
            item.updated_by = user.id
            item.created_at = item.created_at or item.updated_at
            item.created_by = item.created_by or item.updated_by
            records.append((json.dumps(vars(item)),))

        namespace = f"{tenant.slug}.{self.table}"
        query = f"""
            INSERT INTO {namespace}(data) (
                SELECT *
                FROM unnest($1::{namespace}[]) AS d
            )
            ON CONFLICT ((data->>'id'))
            DO UPDATE SET data = {namespace}.data ||
                EXCLUDED.data - 'created_at' - 'created_by'
            RETURNING *;
        """

        connection = await self.connection_manager.get(tenant.zone)
        rows = await connection.fetch(query, records)

        return [self.constructor(**json.loads(row['data'])) for row in rows]

    async def search(self, domain: QueryDomain, limit=10000, offset=0,
                     order_by=None) -> List[T]:

        tenant = self.tenant_provider.tenant
        user = self.auth_provider.user

        filter, parameters = self.parser.parse(
            domain, jsonb_collection='data')

        query = f"""
            SELECT data FROM "{tenant.slug}".{self.table}
            WHERE {filter}
            {self._order_by()}
        """

        if limit is not None:
            query = " ".join([query, f"LIMIT {limit}"])
        if offset is not None:
            query = " ".join([query, f"OFFSET {offset}"])

        connection = await self.connection_manager.get(tenant.zone)
        result = await connection.fetch(query, *parameters)

        return [self.constructor(**json.loads(row['data']))
                for row in result]

    async def remove(self, item: Union[T, List[T]]) -> bool:
        if not item:
            return False
        tenant = self.tenant_provider.tenant
        user = self.auth_provider.user
        items = item if isinstance(item, list) else [item]
        ids = [item.id for item in items]
        placeholders = ", ".join(f'${i + 1}' for i in range(len(ids)))

        query = f"""
            DELETE FROM "{tenant.slug}".{self.table}
            WHERE (data->>'id') IN ({placeholders});
        """

        connection = await self.connection_manager.get(tenant.zone)
        result = await connection.execute(query, *ids)

        return bool(int(result.replace('DELETE', '')))

    async def count(self, domain: QueryDomain = None) -> int:
        tenant = self.tenant_provider.tenant
        user = self.auth_provider.user

        filter, parameters = self.parser.parse(
            domain, jsonb_collection='data')

        query = f"""
            SELECT count(*) FROM "{tenant.slug}".{self.table}
            WHERE {filter}
        """

        connection = await self.connection_manager.get(tenant.zone)
        count = await connection.fetchval(query, *parameters)

        return count

    def _order_by(self) -> str:
        return "ORDER BY data->>'created_at' DESC NULLS LAST"
