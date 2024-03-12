from datetime import date, datetime
from typing import List
from pydantic import BaseModel


class RoleRequest(BaseModel):
    name: str


class RoleResponse(BaseModel):
    id: int
    name: str


class ImageResponse(BaseModel):
    id: int
    image: bytes


class ImageRequest(BaseModel):
    image: bytes
    product_id: int


class CategoryRequest(BaseModel):
    name: str


class CategoryResponse(BaseModel):
    id: int
    name: str


class ProblemReportRequest(BaseModel):
    description: str
    product_id: int
    user_id: int


class ProblemReportResponse(BaseModel):
    id: int
    description: str
    product_id: int
    user_id: int


class UserRequest(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str
    telephone_number: str
    date_of_birth: date


class UserResponse(BaseModel):
    id: int
    email: str
    password: str
    first_name: str
    last_name: str
    telephone_number: str
    date_of_birth: date
    date_of_registration: datetime


class ProductRequest(BaseModel):
    user_id: int
    title: str
    description: str
    contact_phone: str
    contact_email: str
    price: float
    country: str
    city: str
    street: str


class ProductResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: str
    contact_phone: str
    contact_email: str
    price: float
    country: str
    city: str
    street: str


class ProductResponseShort(BaseModel):
    id: int
    title: str
    price: float
    country: str
    image: int
