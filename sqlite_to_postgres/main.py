from sqlite_to_postgres.config import (BATCH_SIZE, POSTGRES_DSL,
                                       POSTGRES_SCHEMA, SQLITE_DB_PATH, logger)
from sqlite_to_postgres.models import TABLE_TO_CLASS
from sqlite_to_postgres.postgres_service import PostgresService
from sqlite_to_postgres.sqlite_service import SqliteService


def import_data():
    sqlite_loader = SqliteService(SQLITE_DB_PATH, batch_size=BATCH_SIZE)
    postgres_saver = PostgresService(POSTGRES_DSL, POSTGRES_SCHEMA, batch_size=BATCH_SIZE)

    for table_name in TABLE_TO_CLASS.keys():
        offset = 0
        while True:
            logger.info(f'Загрузка данные из {table_name} с оффсетом {offset}')
            data = sqlite_loader.load_data(table_name, offset)

            if not data:
                break

            logger.info(f'Сохранение данных в {table_name}')
            postgres_saver.save_data(table_name, data)
            offset += BATCH_SIZE


if __name__ == '__main__':
    import_data()
