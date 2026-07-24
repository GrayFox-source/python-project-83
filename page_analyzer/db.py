import os

import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError('DATABASE_URL not in the set')
    return psycopg.connect(database_url)

# def init_db():
#     conn = get_db_connection()
#     with conn.cursor() as cursor:
#         cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS urls
#                     (
#                         id SERIAL PRIMARY KEY,
#                         name VARCHAR(255) UNIQUE NOT NULL,
#                         created_at DATE DEFAULT CURRENT_DATE
#                         )
#                     """)
#         cursor.execute("""
#                     CREATE TABLE IF NOT EXISTS url_checks
#                     (
#                         id SERIAL PRIMARY KEY,
#                         url_id INTEGER REFERENCES urls(id),
#                         status_code INTEGER,
#                         h1 TEXT,
#                         title TEXT,
#                         description TEXT,
#                         created_at DATE DEFAULT CURRENT_DATE
#                         )
#                     """)
#     conn.commit()
#     conn.close()