from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, EmailStr

from src.database.models import UserRole


class ContactModel(BaseModel):
    """
    Contact model for creating and updating contacts

    Attributes:
        first_name (str): First name of the contact
        last_name (str): Last name of the contact
        email (str): Email of the contact
        phone_number (str): Phone number of the contact
        birth_date (date): Birth date of the contact
        info (str): Additional information about the contact
    """

    first_name: str = Field(min_length=2, max_length=50)
    last_name: str = Field(min_length=2, max_length=50)
    email: EmailStr = Field(min_length=7, max_length=100)
    phone_number: str = Field(min_length=7, max_length=20)
    birth_date: date
    info: Optional[str] = None


class ContactResponse(ContactModel):
    """
    Contact model for response extends ContactModel

    Attributes:
        id (int): ID of the contact
        created_at (datetime): Creation date of the contact
        updated_at (datetime): Last update date of the contact
    """

    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class User(BaseModel):
    """
    User model for response

    Attributes:
        id (int): ID of the user
        username (str): Username of the user
        email (str): Email of the user
        avatar (str): Avatar of the user
        role (UserRole): Role of the user
    """

    id: int
    username: str
    email: str
    avatar: str
    role: UserRole

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """
    User model for creating a new user

    Attributes:
        username (str): Username of the user
        email (str): Email of the user
        password (str): Password of the user
        role (UserRole): Role of the user (ENUM: admin, user)
    """

    username: str
    email: EmailStr
    password: str = Field(min_length=4, max_length=128)
    role: UserRole


class Token(BaseModel):
    """
    Token model for response

    Attributes:
        access_token (str): Access token
        token_type (str): Type of the token
    """

    access_token: str
    token_type: str


class RequestEmail(BaseModel):
    """
    Request email model for requesting user activation

    Attributes:
        email (str): Email of the user
    """

    email: EmailStr


class ResetPassword(BaseModel):
    """
    Reset password model for resetting user password

    Attributes:
        email (str): Email of the user
        password (str): Password of the user
    """

    email: EmailStr
    password: str = Field(min_length=4, max_length=128, description="Новий пароль")
