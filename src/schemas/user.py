from typing import Optional

from pydantic import BaseModel, Field


class UserBase(BaseModel):
    name: Optional[str] = Field("", description="ユーザーの名前")


class User(UserBase):
    id: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    name: str
    pass
