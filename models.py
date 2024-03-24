from pydantic import BaseModel, EmailStr, PastDate, field_validator
from typing import Optional, Dict
import re


class ContactIn(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: PastDate
    additional_data: Optional[Dict[str, str]] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        if not re.match(r"^\d{9}$", v):
            raise ValueError("Phone number must be a 9-digit number")
        return v


class ContactOut(ContactIn):
    id: int


if __name__ == "__main__":
    # test data
    person_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone_number": "123456789",
        "birth_date": "1990-02-12",
        "additional_data": {"key1": "value1", "key2": "value2"},
    }

    contact1 = ContactIn(**person_data)
    contact2 = ContactOut(id=2, **contact1.model_dump())
    print(contact2.model_dump())
