import psycopg2
from psycopg2 import sql, extras
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

def register_user(telegram_id, full_name):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO bot_users (telegram_id, full_name) VALUES (%s, %s) ON CONFLICT (telegram_id) DO NOTHING",
            (telegram_id, full_name)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Xatolik: {e}")
        return False
    finally:
        cur.close()
        conn.close()

def get_all_books():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT b.title, a.name AS author_name, b.available_copies
        FROM books b
        JOIN authors a ON b.author_id = a.id
        ORDER BY b.title;
    """)
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books

def search_books_by_title(search_term):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=extras.RealDictCursor)
    cur.execute("""
        SELECT b.title, a.name AS author_name, b.available_copies
        FROM books b
        JOIN authors a ON b.author_id = a.id
        WHERE b.title ILIKE %s
    """, (f"%{search_term}%",))
    books = cur.fetchall()
    cur.close()
    conn.close()
    return books