from datetime import date, datetime, UTC

from sqlalchemy import insert, update

from app.dao.base import BaseDao
from app.database import async_session_maker
from app.entries.models import Entries

class EntriesDAO(BaseDao):
    model = Entries

    @classmethod
    async def add(
        cls,
        user_id: int,
        date_start: date,
        date_end: date,
        text: str
    ):
        async with async_session_maker() as session:
            if datetime.now(UTC).timestamp() < datetime.strptime(str(date_start), "%Y-%m-%d").timestamp():
                status = "WAITING"
            elif datetime.now(UTC).timestamp() >= datetime.strptime(str(date_start), "%Y-%m-%d").timestamp():
                status = "WORK"


            entry = insert(Entries).values(
                user_id=user_id,
                date_start=date_start,
                date_end=date_end,
                text=text,
                status=status
            ).returning(Entries)

            entry = await session.execute(entry)
            await session.commit()

            return entry.scalar()

    @classmethod
    async def update(
        cls,
        entry_id: int,
        date_start: date,
        date_end: date,
        text: str
    ):
        async with async_session_maker() as session:

            if datetime.now(UTC).timestamp() < datetime.strptime(str(date_start), "%Y-%m-%d").timestamp():
                status = "WAITING"
            elif datetime.now(UTC).timestamp() >= datetime.strptime(str(date_start), "%Y-%m-%d").timestamp():
                status = "WORK"

            update_entry = update(Entries).where(Entries.id==entry_id).values(
                date_start=date_start,
                date_end=date_end,
                text=text,
                status=status
            ).returning(Entries)

            update_entry = await session.execute(update_entry)
            await session.commit()

            return update_entry.scalar()