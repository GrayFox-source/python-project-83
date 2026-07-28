import os
from datetime import UTC, datetime

import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Подключение к базе данных"""
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL не найден в переменных окружения")
    return psycopg.connect(database_url)

def get_url_by_name(normalized_url: str):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM urls WHERE name = %s", (normalized_url,))
            return cur.fetchone()
    finally:
        conn.close()

def create_url(normalized_url: str) -> int:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (normalized_url, datetime.now(UTC).date())
            )
            return cur.fetchone()[0]
    finally:
        conn.commit()
        conn.close()

def get_url_by_id(url_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, created_at FROM urls WHERE id = %s", (url_id,))
            return cur.fetchone()
    finally:
        conn.close()

def get_all_urls():
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT u.id, u.name, u.created_at, 
                       MAX(uc.created_at) as last_check,
                       (SELECT uc2.status_code
                        FROM url_checks uc2
                        WHERE uc2.url_id = u.id
                        ORDER BY uc2.id DESC LIMIT 1) as last_status
                FROM urls u
                LEFT JOIN url_checks uc ON u.id = uc.url_id
                GROUP BY u.id, u.name, u.created_at
                ORDER BY u.id DESC
            """)
            return cur.fetchall()
    finally:
        conn.close()

def get_checks_by_url_id(url_id: int):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
            """, (url_id,))
            return cur.fetchall()
    finally:
        conn.close()

def create_check(url_id: int, status_code: int, h1: str, title: str, description: str) -> int:
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO url_checks (url_id, status_code, h1, title, description, created_at)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            """, (url_id, status_code, h1, title, description, datetime.now(UTC).date()))
            return cur.fetchone()[0]
    finally:
        conn.commit()
        conn.close()