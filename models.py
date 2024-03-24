from pydantic import BaseModel, EmailStr, PastDate, field_validator
from typing import Optional, Dict
import re


class ContactIn(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
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
