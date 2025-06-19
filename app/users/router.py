# THIRDPARTY
from fastapi import APIRouter, Depends, Response

# FIRSTPARTY
from app.exceptions import (
    IncorrectUserEmailOrPasswordException,
    NotEnoughRightsException,
    NotUserException,
    UserAlreadyExistsException,
)
from app.logger import logger
from app.tasks.tasks import send_registration_email
from app.users.auth import (
    authenticate_user,
    create_access_token,
    get_password_hash,
)
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.users.schemas import SUsers, SUsersAuth

router = APIRouter(prefix="/auth", tags=["Аутентификация & Пользователи"])


@router.post("/register")
async def register(user_data: SUsersAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)

    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)
    logger.info("User successfully registered")

    send_registration_email.delay(user_data.email) # pyright: ignore [reportFunctionMemberAccess]


@router.post("/login")
async def login(response: Response, user_data: SUsersAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectUserEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)

    logger.info("User logged in")

    return {"access_token": access_token}


@router.patch("/admin")
async def change_admin_status(
    user_id: int, admin_status: bool, user: Users = Depends(get_current_user)
) -> SUsers:
    if not user.is_admin:
        raise NotEnoughRightsException

    user = await UserDAO.update_one(user_id, is_admin=admin_status)
    if not user:
        raise NotUserException

    return user # pyright: ignore [reportReturnType]


@router.get("/me")
async def get_me(user: Users = Depends(get_current_user)):
    return user


@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")
    logger.info("User logged out")
