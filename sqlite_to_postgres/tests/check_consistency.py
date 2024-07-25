from dataclasses import asdict
from pathlib import Path
from typing import List

from sqlite_to_postgres.config import (BATCH_SIZE, POSTGRES_DSL,
                                       POSTGRES_SCHEMA, SQLITE_DB_PATH, logger)
from sqlite_to_postgres.models import TABLE_TO_CLASS
from sqlite_to_postgres.postgres_service import PostgresService
from sqlite_to_postgres.sqlite_service import SqliteService

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_DB_PATH = BASE_DIR / SQLITE_DB_PATH


def get_data_from_database(loader, table_name: str) -> List[object]:
    offset = 0
    data = []
    while True:
        batch = loader.load_data(table_name, offset)
        if not batch:
            break
        data.extend(batch)
        offset += len(batch)
    return data


def compare_data(sqlite_data: List[object], postgres_data: List[object], table_name: str):
    sqlite_data_tuples = [tuple(asdict(item).items()) for item in sqlite_data]
    postgres_data_tuples = [tuple(asdict(item).items()) for item in postgres_data]

    for i, sqlite_data_tuple in enumerate(sqlite_data_tuples):
        assert sqlite_data_tuple == postgres_data_tuples[
            i], f'Differences found in {table_name}, \n{sqlite_data_tuple}, \n{postgres_data_tuples[i]}'


def check_data_consistency():
    sqlite_loader = SqliteService(SQLITE_DB_PATH, BATCH_SIZE)
    postgres_loader = PostgresService(POSTGRES_DSL, POSTGRES_SCHEMA, BATCH_SIZE)

    tables = TABLE_TO_CLASS.keys()

    for table in tables:
        logger.info('Comparing data in table %s...', table)
        sqlite_data = get_data_from_database(sqlite_loader, table)
        postgres_data = get_data_from_database(postgres_loader, table)
        compare_data(sqlite_data, postgres_data, table)

    logger.info('Success. No differences found.')


if __name__ == '__main__':
    check_data_consistency()
