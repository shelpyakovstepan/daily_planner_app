# STDLIB
from datetime import date

# THIRDPARTY
from pydantic import BaseModel


class SEntries(BaseModel):
    id: int
    user_id: int
    date_start: date
    date_end: date
    text: str
    status: str
