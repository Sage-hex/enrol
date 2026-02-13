from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1)
    email: EmailStr
    role: Literal["student", "admin"]

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("name must not be empty")
        return value.strip()


class UserRead(UserCreate):
    id: int


class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    requester_role: Literal["student", "admin"]

    @field_validator("title", "code")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field must not be empty")
        return value.strip()


class CourseUpdate(BaseModel):
    title: str = Field(..., min_length=1)
    code: str = Field(..., min_length=1)
    requester_role: Literal["student", "admin"]

    @field_validator("title", "code")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("field must not be empty")
        return value.strip()


class CourseRead(BaseModel):
    id: int
    title: str
    code: str


class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int
    requester_role: Literal["student", "admin"]


class EnrollmentDelete(BaseModel):
    user_id: int
    course_id: int
    requester_role: Literal["student", "admin"]


class EnrollmentRead(BaseModel):
    id: int
    user_id: int
    course_id: int
