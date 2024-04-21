from pydantic import BaseModel, EmailStr, PastDate, field_validator
from typing import Optional
import re


class ContactIn(BaseModel):
    """
    Pydantic model representing input data for creating or updating a contact.

    """

    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birth_date: PastDate
    additional_data: Optional[dict[str, str]] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, v):
        """
        Validate the format of the phone number.

        :param v: The phone number to validate.
        :type v: str

        :return: The validated phone number.
        :rtype: str

        :raises ValueError: If the phone number does not match the expected format.
        """
        if not re.match(r"^\d{9}$", v):
            raise ValueError("Phone number must be a 9-digit number")
        return v


class ContactOut(ContactIn):
    """
    Pydantic model representing output data for retrieving a contact.

    """

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
