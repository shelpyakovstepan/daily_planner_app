# THIRDPARTY
from sqlalchemy.orm import Mapped, mapped_column

# FIRSTPARTY
from app.database import Base


class Users(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(nullable=False, default=False)
