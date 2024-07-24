import logging
import os

from dotenv import load_dotenv

load_dotenv()

BATCH_SIZE = int(os.getenv('BATCH_SIZE', 100))
SQLITE_DB_PATH = os.getenv('SQLITE_DB_PATH')
POSTGRES_SCHEMA = os.getenv('POSTGRES_SCHEMA')
POSTGRES_DSL = {
    'dbname': os.getenv('POSTGRES_DBNAME'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': int(os.getenv('POSTGRES_PORT', 5432)),
}


logger = logging.getLogger('app_logger')
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)
