# STDLIB
from datetime import datetime

# THIRDPARTY
import pytest

# FIRSTPARTY
from app.entries.dao import EntriesDAO


class TestEntriesDAO:
    # @pytest.mark.parametrize(
    #    "user_id,date_start,date_end,text",
    #    [
    #        (1, "2025-06-10", "2100-06-20", "test"),
    #        (2, "2025-06-10", "2100-06-20", "test"),
    #    ],
    # )
    # async def test_add(self, user_id, date_start, date_end, text):
    #    date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
    #    date_end = datetime.strptime(date_end, "%Y-%m-%d").date()
    #
    #    entry = await EntriesDAO.add(user_id, date_start, date_end, text)
    #
    #    assert entry is not None

    @pytest.mark.parametrize(
        "entry_id,date_start,date_end,text",
        [
            (44444, "2025-06-11", "2100-06-21", "test"),
            (44444, "2025-06-10", "2100-06-20", "test_update"),
        ],
    )
    async def test_update(self, entry_id, date_start, date_end, text):
        date_start = datetime.strptime(date_start, "%Y-%m-%d").date()
        date_end = datetime.strptime(date_end, "%Y-%m-%d").date()

        entry = await EntriesDAO.update(entry_id, date_start, date_end, text)

        assert entry is not None
        assert entry.date_start == date_start
        assert entry.date_end == date_end
        assert entry.text == text

    @pytest.mark.parametrize("entry_id,status", [(44444, "READY"), (55555, "READY")])
    async def test_update_one(self, entry_id, status):
        entry = await EntriesDAO.update_one(entry_id, status=status)

        assert entry is not None
        assert str(entry.status) == f"StatusEnum.{status}"

    @pytest.mark.parametrize("entry_id,user_id", [(99999, 11111), (12222, 22222)])
    async def test_delete(self, entry_id, user_id):
        await EntriesDAO.delete(id=entry_id, user_id=user_id)

        delete_entry = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user_id)

        assert delete_entry is None

    @pytest.mark.parametrize(
        "entry_id,user_id,exists",
        [
            (44444, 11111, True),
            (88888, 22222, True),
            (11111, 22222, False),
            (1000000, 11111, False),
        ],
    )
    async def test_find_one_or_none(self, entry_id, user_id, exists):
        entry = await EntriesDAO.find_one_or_none(id=entry_id, user_id=user_id)

        if exists:
            assert entry.id == entry_id
            assert entry.user_id == user_id
        else:
            assert not entry

    @pytest.mark.parametrize("user_id,number_entries", [(11111, 4), (22222, 3)])
    async def test_find_all(self, user_id, number_entries):
        entries = await EntriesDAO.find_all(user_id=user_id)

        assert len(entries) == number_entries


# pyright: reportOptionalMemberAccess=false
