from fastapi import APIRouter, Response

from app.exceptions import UserAlreadyExistsException, IncorrectUserEmailOrPasswordException
from app.users.auth import get_password_hash, authenticate_user, create_access_token
from app.users.dao import UserDAO
from app.users.schemas import SUsersAuth

router = APIRouter(
    prefix="/auth",
    tags=["Аутентификация & Пользователи"]
)

@router.post("/register")
async def register(user_data: SUsersAuth):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)

    await UserDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post("/login")
async def login(response: Response, user_data: SUsersAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectUserEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)

    return {"access_token": access_token}

@router.post("/logout")
def logout_user(response: Response):
    response.delete_cookie("access_token")