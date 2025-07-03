# STDLIB
from datetime import date, datetime

# THIRDPARTY
import pytz
from sqlalchemy import delete, insert, select, update

# FIRSTPARTY
from app.dao.base import BaseDao
from app.database import async_session_maker
from app.entries.models import Entries, StatusEnum
from app.entries.utils import (
    check_availability_by_date_end,
    check_availability_by_date_start_after_date_now,
    check_availability_by_date_start_before_date_now,
)


class EntriesDAO(BaseDao):
    model = Entries

    @classmethod
    async def add(cls, user_id: int, date_start: date, date_end: date, text: str):
        async with async_session_maker() as session:
            if check_availability_by_date_start_after_date_now(date_start):
                status = "WAITING"
            elif check_availability_by_date_start_before_date_now(date_start):
                status = "WORK"

            entry = (
                insert(Entries)
                .values(
                    user_id=user_id,
                    date_start=date_start,
                    date_end=date_end,
                    text=text,
                    status=status,
                )
                .returning(Entries)
            )

            entry = await session.execute(entry)
            await session.commit()

            return entry.scalar()

    @classmethod
    async def update(cls, entry_id: int, date_start: date, date_end: date, text: str):
        async with async_session_maker() as session:

            if check_availability_by_date_start_after_date_now(date_start):
                status = "WAITING"
            elif check_availability_by_date_start_before_date_now(date_start):
                status = "WORK"

            update_entry = (
                update(Entries)
                .where(Entries.id == entry_id)
                .values(
                    date_start=date_start,
                    date_end=date_end,
                    text=text,
                    status=status,
                )
                .returning(Entries)
            )

            update_entry = await session.execute(update_entry)
            await session.commit()

            return update_entry.scalar()

    @classmethod
    async def global_update_statuses(cls):
        async with async_session_maker() as session:
            all_entries = select(Entries)

            all_entries = await session.execute(all_entries)
            all_entries = all_entries.scalars().all()

            for entry in all_entries:
                if (
                    entry.status == StatusEnum.WAITING
                    and check_availability_by_date_start_before_date_now(
                        entry.date_start
                    )
                ):
                    update_entry = (
                        update(Entries)
                        .where(Entries.id == entry.id)
                        .values(status="WORK")
                    )

                    await session.execute(update_entry)

                if entry.status == StatusEnum.WORK and check_availability_by_date_end(
                    entry.date_end
                ):
                    update_entry = (
                        update(Entries)
                        .where(Entries.id == entry.id)
                        .values(status="EXPIRED")
                    )

                    await session.execute(update_entry)

                if (
                    entry.status in (StatusEnum.EXPIRED, StatusEnum.READY)
                    and (
                        datetime.now(pytz.timezone("Europe/Moscow")).date()
                        - datetime.strptime(str(entry.date_end), "%Y-%m-%d").date()
                    ).days
                    >= 15
                ):
                    delete_entry = delete(Entries).where(Entries.id == entry.id)

                    await session.execute(delete_entry)

            await session.commit()


# pyright: reportPossiblyUnboundVariable=false
# pyright: reportIncompatibleMethodOverride=false
# pyright: reportAttributeAccessIssue=false
