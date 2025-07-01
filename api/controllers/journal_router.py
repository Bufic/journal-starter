import logging
from typing import AsyncGenerator
from fastapi import APIRouter, HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from api.repositories.postgres_repository import PostgresDB
from api.services import EntryService
from api.models.entry import Entry


router = APIRouter()

# TODO: Add authentication middleware
# TODO: Add request validation middleware
# TODO: Add rate limiting middleware
# TODO: Add API versioning
# TODO: Add response caching


async def get_entry_service() -> AsyncGenerator[EntryService, None]:

    async with PostgresDB() as db:
        yield EntryService(db)


@router.post("/entries")
async def create_entry(request: Request, entry: Entry, entry_service: EntryService = Depends(get_entry_service)):
    entry_data = entry.model_dump(
        exclude={"id", "created_at", "updated_at", "schema_version"})

    try:
        # create_entry returns the new entry with 'id' as a string
        new_entry = await entry_service.create_entry(entry_data)

    except HTTPException as e:
        if e.status_code == 409:
            raise HTTPException(
                status_code=409, detail="You already have an entry for today."
            )
        raise e

    return JSONResponse(content=jsonable_encoder(new_entry), status_code=201)

# TODO: Implement GET /entries endpoint to list all journal entries
# Example response: [{"id": "123", "work": "...", "struggle": "...", "intention": "..."}]


@router.get("/entries")
async def get_all_entries(request: Request):
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        entries = await entry_service.get_all_entries()
    if not entries:
        raise HTTPException(status_code=404, detail="No entries found")
    return JSONResponse(content=jsonable_encoder(entries), status_code=200)


@router.get("/entries/{entry_id}")
async def get_entry(request: Request, entry_id: str):
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        entry = await entry_service.get_entry(entry_id)
    if not entry:
        raise HTTPException(status_code=404, detail="Entry not found")
    return JSONResponse(content=jsonable_encoder(entry), status_code=200)


@router.patch("/entries/{entry_id}")
async def update_entry(request: Request, entry_id: str, entry_update: dict):
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        result = await entry_service.update_entry(entry_id, entry_update)
    if not result:

        raise HTTPException(status_code=404, detail="Entry not found")

    return result

# TODO: Implement DELETE /entries/{entry_id} endpoint to remove a specific entry
# Return 404 if entry not found


@router.delete("/entries/{entry_id}")
async def delete_entry(request: Request, entry_id: str):
    async with PostgresDB() as db:
        entry_service = EntryService(db)
        result = await entry_service.delete_entry(entry_id)
    if not result:
        raise HTTPException(status_code=404, detail="Entry not found")
    return JSONResponse(content={"detail": "Entry deleted successfully"}, status_code=200)


@router.delete("/entries")
async def delete_all_entries(request: Request):

    async with PostgresDB() as db:
        entry_service = EntryService(db)
        await entry_service.delete_all_entries()

    return {"detail": "All entries deleted"}
