from datetime import date, datetime, UTC
from typing import List

from fastapi import APIRouter, Depends

from app.entries.dao import EntriesDAO
from app.entries.schemas import SEntries
from app.exceptions import NotAddEntryException, NotTrueTimeException, YouDoNotHaveEntriesException, \
    YouDoNotHaveEntryException, TextIsTooBigException
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
    if delta.days < 0 or datetime.now(UTC).timestamp() > datetime.strptime(str(date_end), "%Y-%m-%d").timestamp():
        raise NotTrueTimeException

    if len(text) > 1000:
        raise TextIsTooBigException

    entry = await EntriesDAO.add_entry(user.id, date_start, date_end, text)

    if not entry:
        raise NotAddEntryException
    return entry

@router.get("")
async def get_entries(user: Users = Depends(get_current_user)) -> List[SEntries]:
    entries = await EntriesDAO.find_all(user_id=user.id)
    if not entries:
        raise YouDoNotHaveEntriesException

    return entries

@router.get("/entry_id/")
async def get_entry_by_id(entry_id: int, user: Users = Depends(get_current_user)) -> SEntries:
    entry = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry:
        raise YouDoNotHaveEntryException

    return entry

@router.delete("/{entry_id}")
async def delete_entry(entry_id: int, user: Users = Depends(get_current_user)):
    await EntriesDAO.delete(id=entry_id, user_id=user.id)