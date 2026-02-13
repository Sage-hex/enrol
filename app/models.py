from pydantic import BaseModel, EmailStr
from typing import Literal


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: Literal["student", "admin"]


class Course(BaseModel):
    id: int
    title: str
    code: str


class Enrollment(BaseModel):
    id: int
    user_id: int
    course_id: int
