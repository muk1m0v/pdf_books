import asyncpg
from config import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASS

pool: asyncpg.Pool | None = None


async def init_pool():
    """Создаёт пул соединений и таблицы, если их ещё нет."""
    global pool
    pool = await asyncpg.create_pool(
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
    )
    async with pool.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS active_book, books, users CASCADE;")
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                tg_id BIGINT UNIQUE NOT NULL,
                username TEXT,
                created_at TIMESTAMP DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT NOW()
            );
            """
        )
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS active_book (
                user_id INTEGER PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
                book_id INTEGER REFERENCES books(id) ON DELETE CASCADE
            );
            """
        )


async def close_pool():
    if pool:
        await pool.close()


async def get_or_create_user(tg_id: int, username: str | None) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow("SELECT id FROM users WHERE tg_id = $1", tg_id)
        if row:
            return row["id"]
        row = await conn.fetchrow(
            "INSERT INTO users (tg_id, username) VALUES ($1, $2) RETURNING id",
            tg_id, username,
        )
        return row["id"]


async def save_book(user_id: int, title: str, content: str) -> int:
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            "INSERT INTO books (user_id, title, content) VALUES ($1, $2, $3) RETURNING id",
            user_id, title, content,
        )
        book_id = row["id"]
        await conn.execute(
            """
            INSERT INTO active_book (user_id, book_id) VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET book_id = EXCLUDED.book_id
            """,
            user_id, book_id,
        )
        return book_id


async def get_active_book(user_id: int):
    async with pool.acquire() as conn:
        row = await conn.fetchrow(
            """
            SELECT b.id, b.title, b.content
            FROM active_book a
            JOIN books b ON b.id = a.book_id
            WHERE a.user_id = $1
            """,
            user_id,
        )
        return row


async def get_user_books(user_id: int):
    async with pool.acquire() as conn:
        return await conn.fetch(
            "SELECT id, title, uploaded_at FROM books WHERE user_id = $1 ORDER BY uploaded_at DESC",
            user_id,
        )


async def set_active_book(user_id: int, book_id: int):
    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO active_book (user_id, book_id) VALUES ($1, $2)
            ON CONFLICT (user_id) DO UPDATE SET book_id = EXCLUDED.book_id
            """,
            user_id, book_id,
        )
