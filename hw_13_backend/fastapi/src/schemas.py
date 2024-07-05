import pydantic
from datetime import date
from datetime import datetime


class ContactModel(pydantic.BaseModel):
    first_name: str = pydantic.Field(max_length = 30)
    last_name: str = pydantic.Field(max_length = 30)
    email: pydantic.EmailStr
    phone_number: str = pydantic.Field(max_length = 12)
    birth_date: date


class ContactResponce(ContactModel):
    id: int


class ContactRequest(ContactModel):
    pass


class UserModel(pydantic.BaseModel):
    username: str = pydantic.Field(min_length=5, max_length=16)
    email: str
    password: str = pydantic.Field(min_length=6, max_length=10)


class UserDb(pydantic.BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime
    avatar: str

    class Config:
        orm_mode = True


class UserResponse(pydantic.BaseModel):
    user: UserDb
    detail: str = "User successfully created"


class TokenModel(pydantic.BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(pydantic.BaseModel):
    email: pydantic.EmailStr

