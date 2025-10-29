import psycopg2
import os

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "multipleserver-copy-postgres-1"),
        port=os.getenv("DB_PORT", "5432"),
        user=os.getenv("DB_USER", "tripuser"),
        password=os.getenv("DB_PASSWORD", "trippass"),
        database=os.getenv("DB_NAME", "tripdb"),
    )
