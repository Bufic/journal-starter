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


# import logging
# from typing import Annotated, Optional
# from datetime import datetime
# from fastapi import (
#     APIRouter,
#     HTTPException,
#     Depends,
#     status,
#     Query,
#     Request,
#     Security
# )
# from fastapi.encoders import jsonable_encoder
# from fastapi.security import OAuth2PasswordBearer
# from fastapi_cache.decorator import cache
# from slowapi import Limiter
# from slowapi.util import get_remote_address
# from api.repositories.postgres_repository import PostgresDB
# from api.services import EntryService
# from api.models.entry import Entry, EntryUpdate
# from api.utils.middlewares import RequestValidationMiddleware

# # Initialize rate limiter
# limiter = Limiter(key_func=get_remote_address)
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# router = APIRouter(
#     prefix="/v1/entries",  # API versioning
#     tags=["Journal Entries"],
#     dependencies=[Security(oauth2_scheme)],  # Global auth
#     responses={
#         404: {"description": "Not found"},
#         429: {"description": "Too many requests"},
#         401: {"description": "Unauthorized"}
#     }
# )

# # Add validation middleware
# router.route_class = RequestValidationMiddleware

# logger = logging.getLogger(__name__)


# async def get_entry_service() -> EntryService:
#     """Dependency injection for entry service"""
#     async with PostgresDB() as db:
#         yield EntryService(db)


# @router.post(
#     "/",
#     response_model=Entry,
#     status_code=status.HTTP_201_CREATED,
#     responses={
#         409: {"description": "Entry already exists"},
#         422: {"description": "Validation error"},
#         429: {"description": "Too many requests"}
#     }
# )
# @limiter.limit("5/minute")  # Rate limiting
# async def create_entry(
#     request: Request,  # Required for limiter
#     entry: Entry,
#     entry_service: Annotated[EntryService, Depends(get_entry_service)],
#     token: str = Security(oauth2_scheme)  # Authentication
# ) -> Entry:
#     """
#     Create a new journal entry.
#     - Requires authentication
#     - Rate limited: 5 requests/minute
#     """
#     try:
#         entry_data = entry.model_dump(exclude_unset=True)
#         return await entry_service.create_entry(entry_data)
#     except ValueError as e:
#         logger.error(f"Validation error: {str(e)}")
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=str(e)
#         )


# @router.get(
#     "/",
#     response_model=list[Entry],
#     responses={
#         404: {"description": "No entries found"},
#         429: {"description": "Too many requests"}
#     }
# )
# @cache(expire=60)  # Response caching for 60 seconds
# @limiter.limit("100/minute")
# async def get_all_entries(
#     request: Request,
#     entry_service: Annotated[EntryService, Depends(get_entry_service)],
#     start_date: Optional[datetime] = None,
#     end_date: Optional[datetime] = None,
#     limit: int = Query(100, ge=1, le=1000),
#     token: str = Security(oauth2_scheme)
# ) -> list[Entry]:
#     """
#     Get all journal entries with filters.
#     - Cached for 60 seconds
#     - Rate limited: 100 requests/minute
#     - Requires authentication
#     """
#     entries = await entry_service.get_all_entries(
#         start_date=start_date,
#         end_date=end_date,
#         limit=limit
#     )
#     if not entries:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="No entries found"
#         )
#     return entries


# @router.get(
#     "/{entry_id}",
#     response_model=Entry,
#     responses={
#         404: {"description": "Entry not found"},
#         429: {"description": "Too many requests"}
#     }
# )
# @cache(expire=30)
# async def get_entry(
#     request: Request,
#     entry_id: str,
#     entry_service: Annotated[EntryService, Depends(get_entry_service)],
#     token: str = Security(oauth2_scheme)
# ) -> Entry:
#     """Get specific entry with caching"""
#     if (entry := await entry_service.get_entry(entry_id)) is None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Entry not found"
#         )
#     return entry


# @router.patch(
#     "/{entry_id}",
#     response_model=Entry,
#     responses={
#         404: {"description": "Entry not found"},
#         422: {"description": "Validation error"},
#         429: {"description": "Too many requests"}
#     }
# )
# @limiter.limit("10/minute")
# async def update_entry(
#     request: Request,
#     entry_id: str,
#     entry_update: EntryUpdate,
#     entry_service: Annotated[EntryService, Depends(get_entry_service)],
#     token: str = Security(oauth2_scheme)
# ) -> Entry:
#     """Update entry with rate limiting"""
#     try:
#         if (updated_entry := await entry_service.update_entry(
#             entry_id,
#             entry_update.model_dump(exclude_unset=True)
#         )) is None:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Entry not found"
#             )
#         return updated_entry
#     except ValueError as e:
#         raise HTTPException(
#             status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#             detail=str(e)
#         )


# @router.delete(
#     "/{entry_id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         404: {"description": "Entry not found"},
#         429: {"description": "Too many requests"}
#     }
# )
# @limiter.limit("5/minute")
# async def delete_entry(
#     request: Request,
#     entry_id: str,
#     entry_service: Annotated[EntryService, Depends(get_entry_service)],
#     token: str = Security(oauth2_scheme)
# ) -> None:
#     """Delete entry with authentication"""
#     if not await entry_service.delete_entry(entry_id):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="Entry not found"
#         )


# @router.delete(
#     "/",
#     status_code=status.HTTP_204_NO_CONTENT,
#     responses={
#         403: {"description": "Forbidden"},
#         429: {"description": "Too many requests"}
#     }
# )
# @limiter.limit("1/hour")
# async def delete_all_entries(
#     request: Request,
#     entry_service: Annotated[EntryService, Depends(get_entry_service)],
#     token: str = Security(oauth2_scheme, scopes=[
#                           "admin"])  # Admin scope required
# ) -> None:
#     """Danger zone: Delete all entries (Admin only)"""
#     await entry_service.delete_all_entries()
