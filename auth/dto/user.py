from uuid import UUID

from pydantic import BaseModel

from auth.enums import Role


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    is_active: bool | None = None
    role: Role | None = None


class CreateUser(User):
    username: str
    email: str
    full_name: str
    password: str
    role: Role


class UserInDB(User):
    hashed_password: str
    external_id: UUID
