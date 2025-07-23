import os
import asyncio
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")

# SCHEMA_SQL = """
# DROP TABLE IF EXISTS entries;

# CREATE TABLE entries (
#     id UUID PRIMARY KEY,
#     data JSONB,
#     created_at TIMESTAMPTZ,
#     updated_at TIMESTAMPTZ
# );
# """

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS entries (
    id UUID PRIMARY KEY,
    data JSONB NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


async def init_db():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute(SCHEMA_SQL)
    await conn.close()
    print("✅ Table 'entries' created or replaced.")

if __name__ == "__main__":
    asyncio.run(init_db())
