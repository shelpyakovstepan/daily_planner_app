# STDLIB
from datetime import datetime

# THIRDPARTY
import pytest

# FIRSTPARTY
from app.entries.dao import EntriesDAO


@pytest.mark.parametrize(
    "user_id,date_start,date_end,text",
    [
        (1, "2025-06-10", "2100-06-20", "test"),
        (2, "2025-06-10", "2100-06-20", "test"),
    ],
)
async def test_add(user_id, date_start, date_end, text):
    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    date_end = datetime.strptime(date_end, "%Y-%m-%d").date()

    entry = await EntriesDAO.add(user_id, date_start, date_end, text)

    assert entry is not None


@pytest.mark.parametrize(
    "entry_id,date_start,date_end,text",
    [
        (9, "2025-06-11", "2100-06-21", "test"),
        (10, "2025-06-10", "2100-06-20", "test_update"),
    ],
)
async def test_update(entry_id, date_start, date_end, text):
    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    date_end = datetime.strptime(date_end, "%Y-%m-%d").date()

    entry = await EntriesDAO.update(entry_id, date_start, date_end, text)

    assert entry is not None
    assert entry.date_start == date_start
    assert entry.date_end == date_end
    assert entry.text == text


@pytest.mark.parametrize("entry_id,status", [(4, "READY"), (5, "READY")])
async def test_update_one(entry_id, status):
    entry = await EntriesDAO.update_one(entry_id, status=status)

    assert entry is not None
    assert str(entry.status) == f"StatusEnum.{status}"


@pytest.mark.parametrize("entry_id,user_id", [(9, 1), (10, 2)])
async def test_delete(entry_id, user_id):
    await EntriesDAO.delete(id=entry_id, user_id=user_id)

    delete_entry = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user_id)

    assert delete_entry is None


@pytest.mark.parametrize(
    "entry_id,user_id,exists",
    [(1, 1, True), (5, 2, True), (1, 2, False), (100, 1, False)],
)
async def test_find_one_or_none(entry_id, user_id, exists):
    entry = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user_id)

    if exists:
        assert entry.id == entry_id
        assert entry.user_id == user_id
    else:
        assert not entry


@pytest.mark.parametrize("user_id,number_entries", [(1, 3), (2, 3)])
async def test_find_all(user_id, number_entries):
    entries = await EntriesDAO.find_all(user_id=user_id)

    assert len(entries) == number_entries
