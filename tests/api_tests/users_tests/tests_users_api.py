import pytest
from httpx import AsyncClient

from app.users.auth import authenticate_user


@pytest.mark.parametrize("email,password,status_code", [
    ("pes@kot.com", "pesokot", 200),
    ("pes@kot.com", "pesokot", 409),
    ("kot@pes.com", "kotopes", 200),
    ("step3210shelpyakov@gmail.com", "fff", 409),
    ("abcde", "kotopes", 422)

])
async def test_register_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/register", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("email,password,status_code", [
    ("step3210shelpyakov@gmail.com", "kolobok", 200),
    ("user@example.com", "parol", 200),
    ("step3210shelpyakov@gmail.com", "fff", 401),
    ("abcde", "kotopes", 422),
    ("step@gmail.com", "kolobok", 401),
])
async def test_login_user(email, password, status_code, ac: AsyncClient):
    response = await ac.post("/auth/login", json={
        "email": email,
        "password": password
    })

    assert response.status_code == status_code


@pytest.mark.parametrize("user_id,admin_status,status_code_for_non_admin,status_code_for_admin", [
    (1, True, 403, 200),
    (100, True, 409, 409)
])
async def test_change_admin_status(
        user_id, admin_status, status_code_for_non_admin, status_code_for_admin,
        authenticated_ac: AsyncClient,
        authenticated_ac_admin: AsyncClient
):
    non_admin_user_request_response = await authenticated_ac.patch("/auth/admin", params={
        "user_id": user_id,
        "admin_status": admin_status
    })

    assert non_admin_user_request_response.status_code == status_code_for_non_admin

    admin_user_request_response = await authenticated_ac_admin.patch("/auth/admin", params={
        "user_id": user_id,
        "admin_status": admin_status
    })

    assert admin_user_request_response.status_code == status_code_for_admin


@pytest.mark.parametrize("status_code_for_unauthorized_user,status_code_for_authorized_user", [
    (401, 200)
])
async def test_get_me(
        status_code_for_unauthorized_user, status_code_for_authorized_user,
        ac: AsyncClient,
        authenticated_ac: AsyncClient
):
    unauthorized_user_request_response = await ac.get("/auth/me")
    assert unauthorized_user_request_response.status_code == status_code_for_unauthorized_user

    authorized_user_request_response = await authenticated_ac.get("/auth/me")
    assert authorized_user_request_response.status_code == status_code_for_authorized_user