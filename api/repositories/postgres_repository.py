import json
import os
import uuid
import logging
import asyncpg
from datetime import datetime, timezone
from typing import Any, Dict, List
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from api.repositories.interface_respository import DatabaseInterface

load_dotenv()
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is missing")



class PostgresDB(DatabaseInterface):
    # Custom function to handle datetime serialization
    @staticmethod
    def datetime_serialize(obj):
        """Convert datetime objects to ISO format for JSON serialization."""
        if isinstance(obj, datetime):
                return obj.isoformat()  # Convert datetime to string for JSON
        raise TypeError(f"Type {type(obj)} not serializable")
        
    async def __aenter__(self):
        logger.info("Creating Postgres connection pool.")
        self.pool = await asyncpg.create_pool(DATABASE_URL)
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        logger.info("Closing Postgres connection pool.")
        await self.pool.close()

    async def create_entry(self, entry_data: Dict[str, Any]) -> None:
        logger.info("Creating a new entry in Postgres.")
        async with self.pool.acquire() as conn:
            query = """
            INSERT INTO entries (id, data, created_at, updated_at)
            VALUES ($1, $2, $3, $4)
            """
            entry_id = entry_data.get("id") or str(uuid.uuid4())
            
            # Convert entry_data to JSON with datetime serialization
            data_json = json.dumps(entry_data, default=PostgresDB.datetime_serialize)
            
            await conn.execute(query, entry_id, data_json, entry_data["created_at"], entry_data["updated_at"])
            logger.debug("Entry created with id: %s", entry_id)

    async def get_entries(self) -> List[Dict[str, Any]]:
        logger.debug("Getting all entries from Postgres.")
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM entries"
            rows = await conn.fetch(query)
            # Deserialize JSONB data before returning
            return [
                {
                    **dict(row), 
                    "data": json.loads(row["data"])  # Convert JSON string back to a dictionary
                } 
                for row in rows
            ]
        
    async def get_entry(self, entry_id: str) -> Dict[str, Any]:
        logger.info("Getting entry with id: %s from Postgres", entry_id)
        async with self.pool.acquire() as conn:
            query = "SELECT * FROM entries WHERE id = $1"
            row = await conn.fetchrow(query, entry_id)
            
            if row:
                entry = dict(row)
                entry["data"] = json.loads(entry["data"])  # Deserialize JSONB field
                return entry

            logger.error("Entry with id %s not found in Postgres", entry_id)
            return None
   
    async def update_entry(self, entry_id: str, updated_data: Dict[str, Any]) -> None:
        logger.info("Updating entry with id: %s in Postgres", entry_id)

        # Ensure updated_at is a proper datetime object (not string)
        updated_at = datetime.now(timezone.utc)  # Create a valid datetime object
        
        # Ensure the entry_id is part of the updated data
        updated_data["id"] = entry_id
        updated_data["updated_at"] = updated_at  # Add updated_at to the data

        # Serialize updated data dictionary to JSON, handling datetime serialization
        data_json = json.dumps(updated_data, default=PostgresDB.datetime_serialize)

        # Prepare query for updating the entire row
        async with self.pool.acquire() as conn:
            query = """
            UPDATE entries 
            SET data = $2, updated_at = $3
            WHERE id = $1
            """
            # Execute the update query with the full data (data_json)
            await conn.execute(query, entry_id, data_json, updated_at)  # Pass updated_at separately
            logger.debug("Entry %s updated in Postgres", entry_id)

    async def delete_entry(self, entry_id: str) -> None:
        logger.info("Deleting entry with id %s from Postgres", entry_id)
        async with self.pool.acquire() as conn:
            query = "DELETE FROM entries WHERE id = $1"
            await conn.execute(query, entry_id)
            logger.debug("Entry %s deleted from Postgres", entry_id)

    async def delete_all_entries(self) -> None:
        logger.info("Deleting all entries in Postgres")
        async with self.pool.acquire() as conn:
            query = "DELETE FROM entries"
            await conn.execute(query)
            logger.debug("All entries deleted from Postgres")
