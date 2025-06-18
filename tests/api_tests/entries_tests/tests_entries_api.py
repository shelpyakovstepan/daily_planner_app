# THIRDPARTY
from httpx import AsyncClient
import pytest


@pytest.mark.parametrize(
    "date_start,date_end,text,status_code",
    [
        ("2025-06-10", "2100-06-10", "test", 200),
        ("2025-06-10", "2025-06-10", "test", 400),
        ("2025-06-10", "2025-06-09", "test", 400),
        ("2025-06-10", "2025-06-11", "test", 400),
        ("fddffd", "dfdgdf", "test", 422),
    ],
)
async def test_add_entry(
    date_start, date_end, text, status_code, authenticated_ac: AsyncClient
):

    response = await authenticated_ac.post(
        "/entries/",
        params={"date_start": date_start, "date_end": date_end, "text": text},
    )

    assert response.status_code == status_code


@pytest.mark.parametrize("entries_number,status_code", [(5, 200)])
async def test_get_entries(authenticated_ac: AsyncClient, entries_number, status_code):
    response = await authenticated_ac.get("/entries")

    assert response.status_code == status_code
    assert len(response.json()) == entries_number


@pytest.mark.parametrize(
    "entry_id,status_code",
    [(1, 200), (2, 200), (5, 409), (1000, 409), ("one", 422)],
)
async def test_get_entry_by_id(authenticated_ac: AsyncClient, entry_id, status_code):
    response = await authenticated_ac.get(f"/entries/{entry_id}/")

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "status,entries_number,status_code",
    [
        ("some_wrong_status", 1, 422),
        ("WORK", 2, 200),
        ("WAITING", 2, 200),
        ("READY", 1, 409),
        ("EXPIRED", 1, 200),
    ],
)
async def test_get_entries_by_status(
    authenticated_ac: AsyncClient, status, entries_number, status_code
):
    response = await authenticated_ac.get(f"/entries/status", params={"status": status})

    assert response.status_code == status_code
    assert len(response.json()) == entries_number


@pytest.mark.parametrize(
    "entry_id,date_start,date_end,text,status_code",
    [
        (1, "2025-06-10", "2025-06-10", "test", 400),
        (1, "2025-06-10", "2025-06-09", "test", 400),
        (1, "2025-06-10", "2025-06-11", "test", 400),
        (1000, "2025-06-10", "2100-06-11", "test", 409),
        (1, "fddffd", "dfdgdf", "test", 422),
        (8, "2025-06-10", "2100-06-10", "test", 200),
        (8, "2025-06-10", "2100-06-10", "test", 200),
        (8, "2025-06-11", "2200-06-10", "test_test", 200),
    ],
)
async def test_update_entry(
    authenticated_ac: AsyncClient,
    entry_id,
    date_start,
    date_end,
    text,
    status_code,
):
    response = await authenticated_ac.put(
        f"/entries//",
        params={
            "entry_id": entry_id,
            "date_start": date_start,
            "date_end": date_end,
            "text": text,
        },
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "entry_id,status,status_code",
    [
        (1, "READY", 200),
        (1000, "READY", 409),
        ("one", "READY", 422),
        (1, "EXPIRED", 422),
        (1, "WAITING", 422),
        (1, "some_wrong_status", 422),
        (1, "WORK", 200),
    ],
)
async def test_update_entry_status(
    authenticated_ac: AsyncClient, entry_id, status, status_code
):
    response = await authenticated_ac.patch(
        f"/entries///", params={"entry_id": entry_id, "status": status}
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "entry_id,status_code", [(1000, 409), (5, 409), ("one", 422), (8, 200)]
)
async def test_delete_entry(authenticated_ac: AsyncClient, entry_id, status_code):
    response = await authenticated_ac.delete(
        f"/entries/{entry_id}", params={"entry_id": entry_id}
    )

    assert response.status_code == status_code


async def test_global_update_statuses(ac: AsyncClient):
    response = await ac.patch("/entries////")

    assert response.status_code == 200
