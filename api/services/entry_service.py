# from datetime import datetime, timezone
# from typing import List, Dict, Any
# import logging

# from api.repositories.postgres_repository import PostgresDB

# logger = logging.getLogger("journal")


# class EntryService:
#     def __init__(self, db: PostgresDB):
#         self.db = db
#         logger.debug("EntryService initialized with PostgresDB client.")

#     async def create_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Creates a new entry."""
#         logger.info("Creating entry")
#         now = datetime.now(timezone.utc)
#         entry = {
#             **entry_data,
#             "created_at": now,
#             "updated_at": now
#         }
#         logger.debug("Entry created: %s", entry)
#         return await self.db.create_entry(entry)

#     async def get_entries(self) -> List[Dict[str, Any]]:
#         """Gets all entries."""
#         logger.info("Fetching entries")
#         entries = await self.db.get_entries()
#         logger.debug("Fetched %d entries", len(entries))
#         return entries

#     async def get_all_entries(self) -> List[Dict[str, Any]]:
#         """Gets all entries."""
#         logger.info("Fetching all entries")
#         entries = await self.db.get_entries()
#         logger.debug("Fetched %d entries", len(entries))
#         return entries

#     async def get_entry(self, entry_id: str) -> Dict[str, Any]:
#         """Gets a specific entry."""
#         logger.info("Fetching entry %s", entry_id)
#         entry = await self.db.get_entry(entry_id)
#         if entry:
#             logger.debug("Entry %s found", entry_id)
#         else:
#             logger.warning("Entry %s not found", entry_id)
#         return entry

#     async def update_entry(self, entry_id: str, updated_data: Dict[str, Any]) -> Dict[str, Any]:
#         """Updates an existing entry."""
#         logger.info("Updating entry %s", entry_id)
#         existing_entry = await self.db.get_entry(entry_id)
#         if not existing_entry:
#             logger.warning("Entry %s not found. Update aborted.", entry_id)
#             return None

#         # Ensure 'id' is not passed into data to avoid duplication
#         updated_data.pop("id", None)

#         clean_data = {
#             **updated_data,
#             "updated_at": datetime.now(timezone.utc),
#             "created_at": existing_entry.get("created_at")
#         }

#         updated_entry = await self.db.update_entry(entry_id, clean_data)
#         logger.debug("Entry %s updated", entry_id)
#         return updated_entry

#     async def delete_entry(self, entry_id: str) -> None:
#         """Deletes a specific entry."""
#         logger.info("Deleting entry %s", entry_id)
#         await self.db.delete_entry(entry_id)
#         logger.debug("Entry %s deleted", entry_id)

#     async def delete_all_entries(self) -> None:
#         """Deletes all entries."""
#         logger.info("Deleting all entries")
#         await self.db.delete_all_entries()
#         logger.debug("All entries deleted")

from datetime import datetime, timezone

from typing import List, Dict, Any
import logging
from uuid import UUID, uuid4

from api.repositories.postgres_repository import PostgresDB

logger = logging.getLogger("journal")


class EntryService:
    def __init__(self, db: PostgresDB):
        self.db = db
        logger.debug("EntryService initialized with PostgresDB client.")

    async def create_entry(self, entry_data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates a new entry."""
        logger.info("Creating entry")
        now = datetime.now(timezone.utc)
        entry = {
            **entry_data,
            "id": str(uuid4()),  # Ensure ID exists before DB
            "created_at": now,
            "updated_at": now
        }
        logger.debug("Entry created: %s", entry)
        return await self.db.create_entry(entry)

    async def get_entries(self) -> List[Dict[str, Any]]:
        """Gets all entries."""
        logger.info("Fetching entries")
        entries = await self.db.get_entries()
        logger.debug("Fetched %d entries", len(entries))
        return entries

    async def get_all_entries(self) -> List[Dict[str, Any]]:
        """Gets all entries."""
        logger.info("Fetching all entries")
        entries = await self.db.get_entries()
        logger.debug("Fetched %d entries", len(entries))
        return entries

    async def get_entry(self, entry_id: UUID) -> Dict[str, Any]:
        """Gets a specific entry."""
        logger.info("Fetching entry %s", entry_id)
        entry = await self.db.get_entry(entry_id)
        if entry:
            logger.debug("Entry %s found", entry_id)
        else:
            logger.warning("Entry %s not found", entry_id)
        return entry

    async def update_entry(self, entry_id: UUID, updated_data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates an existing entry."""
        logger.info("Updating entry %s", entry_id)
        existing_entry = await self.db.get_entry(entry_id)
        if not existing_entry:
            logger.warning("Entry %s not found. Update aborted.", entry_id)
            return None

        # Ensure 'id' is not passed into data to avoid duplication
        updated_data.pop("id", None)

        clean_data = {
            **updated_data,
            "updated_at": datetime.now(timezone.utc),
            "created_at": existing_entry.get("created_at")
        }

        updated_entry = await self.db.update_entry(entry_id, clean_data)
        logger.debug("Entry %s updated", entry_id)
        return updated_entry

    async def delete_entry(self, entry_id: UUID) -> bool:
        """Deletes a specific entry."""
        logger.info("Deleting entry %s", entry_id)
        result = await self.db.delete_entry(entry_id)
        if result:
            logger.debug("Entry %s deleted", entry_id)
        else:
            logger.warning("Entry %s not found. Deletion aborted.", entry_id)
        return result

    async def delete_all_entries(self) -> None:
        """Deletes all entries."""
        logger.info("Deleting all entries")
        await self.db.delete_all_entries()
        logger.debug("All entries deleted")
