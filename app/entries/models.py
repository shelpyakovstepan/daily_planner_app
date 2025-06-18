# STDLIB
import enum

# THIRDPARTY
from sqlalchemy import Column, Date, ForeignKey, Integer, Text
from sqlalchemy.dialects import postgresql

# FIRSTPARTY
from app.database import Base


class StatusEnum(enum.Enum):
    WORK = 1
    READY = 2
    EXPIRED = 3
    WAITING = 4


class Entries(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=False)
    text = Column(Text, nullable=False)
    status = Column(postgresql.ENUM(StatusEnum), nullable=False)
