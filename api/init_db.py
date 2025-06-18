import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")

CREATE_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS entries (
    id UUID PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL,
    updated_at TIMESTAMPTZ NOT NULL
)
"""


async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(CREATE_TABLE_QUERY)
    await conn.close()
    print("✅ Table 'entries' ensured.")

if __name__ == "__main__":
    asyncio.run(init_db())
