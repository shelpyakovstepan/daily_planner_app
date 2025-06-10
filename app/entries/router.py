from datetime import date, datetime, UTC

from fastapi import APIRouter, Depends

from app.entries.dao import EntriesDAO
from app.entries.schemas import SEntries
from app.exceptions import NotAddEntryException, NotTrueTimeException
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/entries",
    tags=["Записи"]
)

@router.post("")
async def add_entry(
        date_start: date, date_end: date, text: str,
        user: Users = Depends(get_current_user)
) -> SEntries:
    delta = date_end - date_start
    if delta.days < 0 or datetime.now(UTC).timestamp() > datetime.strptime(str(date_end), "%Y-%m-%d").timestamp():
        raise NotTrueTimeException

    entry = await EntriesDAO.add_entry(user.id, date_start, date_end, text)

    if not entry:
        raise NotAddEntryException
    return entry