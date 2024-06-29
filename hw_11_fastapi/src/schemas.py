import pydantic
from datetime import date

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

