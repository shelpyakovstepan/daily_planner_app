from datetime import date, datetime, UTC
from typing import List, Literal

from fastapi import APIRouter, Depends

from app.entries.dao import EntriesDAO
from app.entries.schemas import SEntries
from app.exceptions import NotAddEntryException, NotTrueTimeException, YouDoNotHaveEntriesException, \
    YouDoNotHaveEntryException, TextIsTooBigException, NotUpdateEntryException
from app.logger import logger
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/entries",
    tags=["Записи"]
)

@router.post("/")
async def add_entry(
        date_start: date, date_end: date, text: str,
        user: Users = Depends(get_current_user)
) -> SEntries:

    delta = date_end - date_start
    if delta.days <= 0 or datetime.now(UTC).date() >= datetime.strptime(str(date_end), "%Y-%m-%d").date():
        raise NotTrueTimeException

    if len(text) > 1000:
        raise TextIsTooBigException

    entry = await EntriesDAO.add(user.id, date_start, date_end, text)

    if not entry:
        raise NotAddEntryException

    logger.info("Entry successfully added")
    return entry

@router.get("")
async def get_entries(user: Users = Depends(get_current_user)) -> List[SEntries]:
    entries = await EntriesDAO.find_all(user_id=user.id)
    if not entries:
        raise YouDoNotHaveEntriesException

    return entries

@router.get("/{entry_id}/")
async def get_entry_by_id(entry_id: int, user: Users = Depends(get_current_user)) -> SEntries:
    entry = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry:
        raise YouDoNotHaveEntryException

    return entry

@router.get("/status")
async def get_entries_by_status(status: Literal["WAITING", "WORK", "READY", "EXPIRED"], user: Users = Depends(get_current_user)) -> List[SEntries]:
    entries = await EntriesDAO.find_all(status=status, user_id=user.id)

    if not entries:
        raise YouDoNotHaveEntryException
    return entries

@router.put("//")
async def update_entry(
        entry_id: int,
        date_start: date,
        date_end: date,
        text: str,
        user: Users = Depends(get_current_user)
) -> SEntries:

    delta = date_end - date_start
    if delta.days < 0 or datetime.now(UTC).date() >= datetime.strptime(str(date_end), "%Y-%m-%d").date():
        raise NotTrueTimeException

    if len(text) > 1000:
        raise TextIsTooBigException

    entry_update = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry_update:
        raise YouDoNotHaveEntryException

    entry = await EntriesDAO.update(entry_id, date_start=date_start, date_end=date_end, text=text)
    if not entry:
        raise NotUpdateEntryException

    logger.info("Entry successfully updated")
    return entry

@router.patch("///")
async def update_entry_status(
        entry_id: int,
        status: Literal["WORK", "READY"],
        user: Users = Depends(get_current_user)
) -> SEntries:

    entry_update = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry_update:
        raise YouDoNotHaveEntryException

    status_update = await EntriesDAO.update_one(entry_id, status=status)

    logger.info("Entry status successfully updated")
    return status_update

@router.delete("/{entry_id}")
async def delete_entry(entry_id: int, user: Users = Depends(get_current_user)):
    entry_delete = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry_delete:
        raise YouDoNotHaveEntryException

    await EntriesDAO.delete(id=entry_id, user_id=user.id)
    logger.info("Entry successfully deleted")

@router.patch("////")
async def global_update_statuses():
    await EntriesDAO.global_update_statuses()