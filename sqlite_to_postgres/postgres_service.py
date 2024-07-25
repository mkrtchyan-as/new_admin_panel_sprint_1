from dataclasses import asdict, fields
from typing import List

import psycopg
from psycopg.rows import dict_row

from sqlite_to_postgres.models import TABLE_TO_CLASS
from sqlite_to_postgres.utils import rows_to_dataclass


class PostgresService:
    def __init__(self, dsl: dict, schema_name: str, batch_size: int = 1000):
        self.dsl = dsl
        self.batch_size = batch_size
        self.schema_name = schema_name

    def save_data(self, table_name: str, data: List[object]):
        with psycopg.connect(**self.dsl, row_factory=dict_row) as conn:
            with conn.cursor() as cursor:
                dataclass_type = TABLE_TO_CLASS.get(table_name)
                if dataclass_type is None:
                    raise ValueError(f'Missing dataclass for table {table_name}')

                dict_data = [asdict(item) for item in data]
                columns = ', '.join(dict_data[0].keys())
                placeholders = ', '.join(['%s'] * len(dict_data[0]))
                query = (f'INSERT INTO {self.schema_name}.{table_name} ({columns}) VALUES ({placeholders}) '
                         f'ON CONFLICT (id) DO NOTHING')

                for i in range(0, len(dict_data), self.batch_size):
                    batch = dict_data[i:i + self.batch_size]
                    cursor.executemany(query, [tuple(item.values()) for item in batch])
                    conn.commit()

    def load_data(self, table_name: str, offset: int = 0) -> List[object]:
        with psycopg.connect(**self.dsl) as conn:
            with conn.cursor() as cursor:
                dataclass_type = TABLE_TO_CLASS.get(table_name)
                if dataclass_type is None:
                    raise ValueError(f'Missing dataclass for table {table_name}')

                class_fields = ','.join([x.name for x in fields(dataclass_type)])
                cursor.execute(
                    f'SELECT {class_fields} FROM {self.schema_name}.{table_name} OFFSET %s LIMIT %s',
                    (offset,
                     self.batch_size))
                rows = cursor.fetchall()

                return rows_to_dataclass(dataclass_type, rows)
