import sqlite3
from contextlib import contextmanager
from dataclasses import fields
from typing import List

from sqlite_to_postgres.config import logger
from sqlite_to_postgres.models import TABLE_TO_CLASS


class SqliteService:
    def __init__(self, db_path: str, batch_size: int = 1000):
        self.db_path = db_path
        self.batch_size = batch_size

    @contextmanager
    def conn_context(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            yield conn
        except sqlite3.Error as e:
            logger.error('Cannot connect to sqlite db: %s', e)
        finally:
            conn.close()

    def load_data(self, table_name: str, offset: int = 0) -> List[object]:
        with self.conn_context() as conn:
            dataclass_type = TABLE_TO_CLASS.get(table_name)
            class_fields = ','.join([x.name for x in fields(dataclass_type)])

            cursor = conn.cursor()
            cursor.execute(
                f'SELECT {class_fields} FROM {table_name} LIMIT ? OFFSET ?',
                (self.batch_size,
                 offset))
            rows = cursor.fetchall()

            if dataclass_type is None:
                raise ValueError(f'Missing dataclass for table {table_name}')

            return [dataclass_type(*row) for row in rows]
