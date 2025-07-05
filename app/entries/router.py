# STDLIB
from datetime import date, datetime
from typing import List, Literal, Optional

# THIRDPARTY
from fastapi import APIRouter, Depends, Query
import pytz

# FIRSTPARTY
from app.entries.dao import EntriesDAO
from app.entries.models import StatusEnum
from app.entries.schemas import SEntries
from app.entries.utils import check_availability_by_date_end, check_delta_days
from app.exceptions import (
    NotAddEntryException,
    NotTrueTimeException,
    NotUpdateEntryException,
    TextIsTooBigException,
    YouCanNotUpdateEntryException,
    YouDoNotHaveEntriesException,
    YouDoNotHaveEntryException,
)
from app.logger import logger
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(prefix="/entries", tags=["Записи"])


@router.post("/")
async def add_entry(
    date_end: date,
    text: str,
    date_start: Optional[date] = Query(
        datetime.now(pytz.timezone("Europe/Moscow")).date()
    ),
    user: Users = Depends(get_current_user),
) -> SEntries:
    """Создаёт новую запись."""
    if check_delta_days(date_start, date_end) or check_availability_by_date_end(
        date_end
    ):
        raise NotTrueTimeException

    if len(text) > 1000:
        raise TextIsTooBigException

    entry = await EntriesDAO.add(
        user.id,
        date_start,
        date_end,
        text,  # pyright: ignore [reportArgumentType]
    )

    if not entry:
        raise NotAddEntryException

    logger.info("Entry successfully added")
    return entry


@router.get("")
async def get_entries(
    user: Users = Depends(get_current_user),
) -> List[SEntries]:
    """Выдаёт все записи пользователя."""
    entries = await EntriesDAO.find_all(user_id=user.id)
    if not entries:
        raise YouDoNotHaveEntriesException

    return entries


@router.get("/{entry_id}/")
async def get_entry_by_id(
    entry_id: int, user: Users = Depends(get_current_user)
) -> SEntries:
    """Выдаёт запись пользователя по id."""
    entry = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry:
        raise YouDoNotHaveEntryException

    return entry


@router.get("/status")
async def get_entries_by_status(
    status: Literal["WAITING", "WORK", "READY", "EXPIRED"],
    user: Users = Depends(get_current_user),
) -> List[SEntries]:
    """Выдаёт все записи пользователя по статусу."""
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
    user: Users = Depends(get_current_user),
) -> SEntries:
    """Обновляет существующую запись."""
    if check_delta_days(date_start, date_end) or check_availability_by_date_end(
        date_end
    ):
        raise NotTrueTimeException

    if len(text) > 1000:
        raise TextIsTooBigException

    entry_update = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry_update:
        raise YouDoNotHaveEntryException

    if (
        entry_update.status == StatusEnum.EXPIRED
        or entry_update.status == StatusEnum.READY
    ):
        raise YouCanNotUpdateEntryException

    entry = await EntriesDAO.update(
        entry_id, date_start=date_start, date_end=date_end, text=text
    )
    if not entry:
        raise NotUpdateEntryException

    logger.info("Entry successfully updated")
    return entry


@router.patch("///")
async def update_entry_status(
    entry_id: int,
    status: Literal["WORK", "READY"],
    user: Users = Depends(get_current_user),
) -> SEntries:
    """Обновляет статус существующей записи (WORK/READY)."""
    entry_update = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry_update:
        raise YouDoNotHaveEntryException

    if (
        entry_update.status == StatusEnum.EXPIRED
        or entry_update.status == StatusEnum.WAITING
    ):
        raise YouCanNotUpdateEntryException

    if check_availability_by_date_end(entry_update.date_end):
        raise NotTrueTimeException

    status_update = await EntriesDAO.update_one(entry_id, status=status)

    logger.info("Entry status successfully updated")
    return status_update


@router.delete("/{entry_id}")
async def delete_entry(entry_id: int, user: Users = Depends(get_current_user)):
    """Удаляет запись."""
    entry_delete = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user.id)
    if not entry_delete:
        raise YouDoNotHaveEntryException

    await EntriesDAO.delete(id=entry_id, user_id=user.id)
    logger.info("Entry successfully deleted")


@router.patch("////")
async def global_update_statuses():
    """Обновляет или удаляет все записи в зависимости от их статуса и даты."""
    await EntriesDAO.global_update_statuses()


# pyright: reportReturnType=false
