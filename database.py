import psycopg2
import os
from dotenv import load_dotenv
from contextlib import contextmanager

load_dotenv()

DATABASE_CONFIG = {
    'dbname': os.getenv("DB_NAME"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': os.getenv("DB_PORT"),
    'sslmode': "require",
    'channel_binding': "require"
}

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = psycopg2.connect(**DATABASE_CONFIG)
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()
