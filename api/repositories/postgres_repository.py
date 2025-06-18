# import json
# import os
# from datetime import datetime, timezone
# from typing import Any, Dict, List
# from dotenv import load_dotenv
# import asyncpg
# from api.repositories.interface_respository import DatabaseInterface

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is missing")


# class PostgresDB(DatabaseInterface):
#     @staticmethod
#     def datetime_serialize(obj):
#         """Convert datetime objects to ISO format for JSON serialization."""
#         if isinstance(obj, datetime):
#             return obj.isoformat()
#         raise TypeError(f"Type {type(obj)} not serializable")

#     async def __aenter__(self):
#         self.pool = await asyncpg.create_pool(DATABASE_URL)
#         return self

#     async def __aexit__(self, exc_type, exc_value, traceback):
#         await self.pool.close()

#     async def create_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
#         async with self.pool.acquire() as conn:
#             query = """
#             INSERT INTO entries (data, created_at, updated_at)
#             VALUES ($1, $2, $3)
#             RETURNING id, data, created_at, updated_at
#             """

#             created_at = entry_data.get(
#                 "created_at") or datetime.now(timezone.utc)
#             updated_at = entry_data.get("updated_at") or created_at

#             data_json = json.dumps(
#                 entry_data, default=PostgresDB.datetime_serialize)
#             row = await conn.fetchrow(query, data_json, created_at, updated_at)

#             if row:
#                 result = dict(row)
#                 result["data"] = json.loads(result["data"])
#                 # Cast ID to string for API consistency
#                 result["id"] = str(result["id"])
#                 return result

#             raise Exception("Failed to insert entry")

#     async def get_entries(self) -> List[Dict[str, Any]]:
#         async with self.pool.acquire() as conn:
#             query = "SELECT * FROM entries"
#             rows = await conn.fetch(query)
#             return [
#                 {
#                     **dict(row),
#                     "data": json.loads(row["data"]),
#                     "id": str(row["id"])  # Cast to string
#                 }
#                 for row in rows
#             ]

#     async def get_entry(self, entry_id: str) -> Dict[str, Any]:
#         async with self.pool.acquire() as conn:
#             query = "SELECT * FROM entries WHERE id = $1"
#             try:
#                 int_id = int(entry_id)
#             except ValueError:
#                 return None  # or raise exception if you want

#             row = await conn.fetchrow(query, int_id)
#             if row:
#                 entry = dict(row)
#                 entry["data"] = json.loads(entry["data"])
#                 entry["id"] = str(entry["id"])  # Cast to string
#                 return entry
#             return None

#     async def update_entry(self, entry_id: str, updated_data: Dict[str, Any]) -> Dict[str, Any]:
#         async with self.pool.acquire() as conn:
#             updated_at = datetime.now(timezone.utc)
#             updated_data["updated_at"] = updated_at

#             data_json = json.dumps(
#                 updated_data, default=PostgresDB.datetime_serialize)

#             try:
#                 int_id = int(entry_id)
#             except ValueError:
#                 return None

#             query = """
#             UPDATE entries
#             SET data = $2, updated_at = $3
#             WHERE id = $1
#             RETURNING id, data, created_at, updated_at
#             """
#             row = await conn.fetchrow(query, int_id, data_json, updated_at)

#             if row:
#                 result = dict(row)
#                 result["data"] = json.loads(result["data"])
#                 result["id"] = str(result["id"])
#                 return result

#             return None

#     async def delete_entry(self, entry_id: str) -> bool:
#         async with self.pool.acquire() as conn:
#             try:
#                 int_id = int(entry_id)
#             except ValueError:
#                 return False

#             query = "DELETE FROM entries WHERE id = $1"
#             result = await conn.execute(query, int_id)
#             # result is like 'DELETE 1' if deleted, 'DELETE 0' if not
#             return result.endswith("1")

#     async def delete_all_entries(self) -> None:
#         async with self.pool.acquire() as conn:
#             query = "DELETE FROM entries"
#             await conn.execute(query)

# import json
# import os
# from datetime import datetime, timezone
# from typing import Any, Dict, List
# from uuid import UUID, uuid4
# from dotenv import load_dotenv
# import asyncpg
# from api.repositories.interface_respository import DatabaseInterface

# load_dotenv()

# DATABASE_URL = os.getenv("DATABASE_URL")
# if not DATABASE_URL:
#     raise ValueError("DATABASE_URL environment variable is missing")


# class PostgresDB(DatabaseInterface):
#     @staticmethod
#     def datetime_serialize(obj):
#         """Convert datetime objects to ISO format for JSON serialization."""
#         if isinstance(obj, datetime):
#             return obj.isoformat()
#         raise TypeError(f"Type {type(obj)} not serializable")

#     async def __aenter__(self):
#         self.pool = await asyncpg.create_pool(DATABASE_URL)
#         return self

#     async def __aexit__(self, exc_type, exc_value, traceback):
#         await self.pool.close()

#     async def create_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
#         async with self.pool.acquire() as conn:
#             query = """
#             INSERT INTO entries (id, data, created_at, updated_at)
#             VALUES ($1, $2, $3, $4)
#             RETURNING id, data, created_at, updated_at
#             """

#         entry_id = entry_data.get("id") or str(uuid4())
#         created_at = entry_data.get("created_at") or datetime.now(timezone.utc)
#         updated_at = entry_data.get("updated_at") or created_at

#         data_json = json.dumps(entry_data, default=self.datetime_serialize)

#         row = await conn.fetchrow(
#             query,
#             entry_id,  # Pass UUID directly
#             data_json,
#             created_at,
#             updated_at
#         )

#         if row:
#             result = dict(row)
#             result["data"] = json.loads(result["data"])
#             return result

#         raise Exception("Failed to insert entry")

#     async def get_entries(self) -> List[Dict[str, Any]]:
#         async with self.pool.acquire() as conn:
#             query = "SELECT * FROM entries"
#             rows = await conn.fetch(query)
#             return [
#                 {
#                     **dict(row),
#                     "data": json.loads(row["data"]),
#                     "id": str(row["id"])
#                 }
#                 for row in rows
#             ]

#     async def get_entry(self, entry_id: UUID) -> Dict[str, Any]:
#         async with self.pool.acquire() as conn:
#             query = "SELECT * FROM entries WHERE id = $1"
#             row = await conn.fetchrow(query, entry_id)
#             if row:
#                 entry = dict(row)
#                 entry["data"] = json.loads(entry["data"])
#                 entry["id"] = str(entry["id"])
#                 return entry
#             return None

#     async def update_entry(self, entry_id: UUID, updated_data: Dict[str, Any]) -> Dict[str, Any]:
#         async with self.pool.acquire() as conn:
#             updated_at = datetime.now(timezone.utc)
#             updated_data["updated_at"] = updated_at

#             data_json = json.dumps(
#                 updated_data, default=PostgresDB.datetime_serialize)

#             query = """
#             UPDATE entries
#             SET data = $2, updated_at = $3
#             WHERE id = $1
#             RETURNING id, data, created_at, updated_at
#             """
#             row = await conn.fetchrow(query, entry_id, data_json, updated_at)

#             if row:
#                 result = dict(row)
#                 result["data"] = json.loads(result["data"])
#                 result["id"] = str(result["id"])
#                 return result

#             return None

#     async def delete_entry(self, entry_id: UUID) -> bool:
#         async with self.pool.acquire() as conn:
#             query = "DELETE FROM entries WHERE id = $1"
#             result = await conn.execute(query, entry_id)
#             return result.endswith("1")

#     async def delete_all_entries(self) -> None:
#         async with self.pool.acquire() as conn:
#             query = "DELETE FROM entries"
#             await conn.execute(query)

import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List
from uuid import UUID, uuid4
from dotenv import load_dotenv
import asyncpg
from api.repositories.interface_respository import DatabaseInterface

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")


class PostgresDB(DatabaseInterface):
    @staticmethod
    def datetime_serialize(obj):
        """Convert datetime objects to ISO format for JSON serialization."""
        if isinstance(obj, datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")

    async def __aenter__(self):
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.pool.close()

    async def create_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        entry_id = entry_data.get("id") or str(uuid4())
        created_at = entry_data.get("created_at") or datetime.now(timezone.utc)
        updated_at = entry_data.get("updated_at") or created_at

        data_json = json.dumps(entry_data, default=self.datetime_serialize)

        async with self.pool.acquire() as conn:
            query = """
            INSERT INTO entries (id, data, created_at, updated_at)
            VALUES ($1, $2, $3, $4)
            RETURNING id, data, created_at, updated_at
            """
            row = await conn.fetchrow(
                query,
                entry_id,
                data_json,
                created_at,
                updated_at
            )

        if row:
            result = dict(row)
            result["data"] = json.loads(result["data"])
            return result

        raise Exception("Failed to insert entry")

    async def get_entries(self) -> List[Dict[str, Any]]:
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM entries"
            rows = await conn.fetch(query)
            return [
                {
                    **dict(row),
                    "data": json.loads(row["data"]),
                    "id": str(row["id"])
                }
                for row in rows
            ]

    async def get_entry(self, entry_id: UUID) -> Dict[str, Any]:
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM entries WHERE id = $1"
            row = await conn.fetchrow(query, entry_id)
            if row:
                entry = dict(row)
                entry["data"] = json.loads(entry["data"])
                entry["id"] = str(entry["id"])
                return entry
            return None

    async def update_entry(self, entry_id: UUID, updated_data: Dict[str, Any]) -> Dict[str, Any]:
        updated_at = datetime.now(timezone.utc)
        updated_data["updated_at"] = updated_at

        data_json = json.dumps(
            updated_data, default=PostgresDB.datetime_serialize)

        async with self.pool.acquire() as conn:
            query = """
            UPDATE entries 
            SET data = $2, updated_at = $3
            WHERE id = $1
            RETURNING id, data, created_at, updated_at
            """
            row = await conn.fetchrow(query, entry_id, data_json, updated_at)

        if row:
            result = dict(row)
            result["data"] = json.loads(result["data"])
            result["id"] = str(result["id"])
            return result

        return None

    async def delete_entry(self, entry_id: UUID) -> bool:
        async with self.pool.acquire() as conn:
            query = "DELETE FROM entries WHERE id = $1"
            result = await conn.execute(query, entry_id)
            return result.endswith("1")

    async def delete_all_entries(self) -> None:
        async with self.pool.acquire() as conn:
            query = "DELETE FROM entries"
            await conn.execute(query)
