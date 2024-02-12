from pydantic import BaseModel
from typing import Literal, Optional


class SeedOrdersInput(BaseModel):
    count: Optional[int] = 500


class GroupOrdersInput(BaseModel):
    algorithm: Literal['kmeans', 'kmeans-constrained']
    group_count: Optional[int] = 20


class GroupedPoint():
    x: float
    y: float
    group: int


class OrderSchema(BaseModel):
    id: int
    lat: float
    lon: float
    address: Optional[str] = None
    group: Optional[int] = None


class CreateOrderSchema(BaseModel):
    lat: float
    lon: float
    address: Optional[int] = None
    group: Optional[int] = None
