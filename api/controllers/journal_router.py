import logging
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from api.repositories.postgres_repository import PostgresDB
from api.services import EntryService

logger = logging.getLogger(__name__)
router = APIRouter()

async def get_entry_service() -> AsyncGenerator[EntryService, None]:
    logger.debug("Creating EntryService dependency")
    async with PostgresDB() as db:
        yield EntryService(db)

@router.post("/entries/")
async def create_entry(request: Request, entry: dict, entry_service: EntryService = Depends(get_entry_service)):
    logger.info("Create daily entry requested")
    entry_data = {
        k: v for k, v in entry.items()
        if k not in ['id', 'created_at', 'updated_at']
    }
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        try:
            enriched_entry = await entry_service.create_entry(entry_data)
            await entry_service.db.create_entry(enriched_entry)
            logger.info("Daily entry created successfully")
        except HTTPException as e:
            logger.error("HTTPException during entry creation: %s", e.detail)
            if e.status_code == 409:
                raise HTTPException(
                    status_code=409, detail="You already have an entry for today."
                )
            raise e
    return JSONResponse(content={"detail": "Entry created successfully"}, status_code=201)

@router.get("/entries")
async def get_all_entries(request: Request):
    logger.info("Fetching all entries")
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        entries = await entry_service.get_all_entries()
    logger.debug("Retrieved %d entries", len(entries))
    return entries

@router.get("/entries/{entry_id}")
async def get_entry(request: Request, entry_id: str):
    logger.info("Fetching entry with id '%s'", entry_id)
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        entry = await entry_service.get_entry(entry_id)
    if not entry:
        logger.warning("Entry with id '%s' not found", entry_id)
        raise HTTPException(status_code=404, detail="Entry not found")
    logger.debug("Entry retrieved: %s", entry)
    return entry

@router.patch("/entries/{entry_id}")
async def update_entry(request: Request, entry_id: str, entry_update: dict):
    logger.info("Update requested for entry id '%s'", entry_id)
    # Directly use the provided update dict without type-based validation
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        result = await entry_service.update_entry(entry_id, entry_update)
    if not result:
        logger.warning("Update failed; entry with id '%s' not found", entry_id)
        raise HTTPException(status_code=404, detail="Entry not found")
    logger.info("Entry with id '%s' updated successfully", entry_id)
    return result

@router.delete("/entries/{entry_id}")
async def delete_entry(request: Request, entry_id: str):
    logger.info("Delete requested for entry id '%s'", entry_id)
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        await entry_service.delete_entry(entry_id)
    logger.info("Entry with id '%s' deleted", entry_id)
    return {"detail": "Entry deleted"}

@router.delete("/entries")
async def delete_all_entries(request: Request):
    logger.info("Delete all entries requested")
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        await entry_service.delete_all_entries()
    logger.info("All entries deleted")
    return {"detail": "All entries deleted"}