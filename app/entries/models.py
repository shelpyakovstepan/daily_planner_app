# STDLIB
from datetime import date
import enum

# THIRDPARTY
from sqlalchemy import ForeignKey, Text
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column

# FIRSTPARTY
from app.database import Base


class StatusEnum(enum.Enum):
    WORK = 1
    READY = 2
    EXPIRED = 3
    WAITING = 4


class Entries(Base):
    __tablename__ = "entries"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    date_start: Mapped[date] = mapped_column(nullable=False)
    date_end: Mapped[date] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[StatusEnum] = mapped_column(
        postgresql.ENUM(StatusEnum), nullable=False
    )
