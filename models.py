from pydantic import BaseModel, Field
from datetime import datetime


class Flight(BaseModel):
    # from: String,
    # to: String,
    type: str = Field(
        title='тип транспорта', max_length=255
    )
    departure: datetime
    duration: int = F
    arrival: datetime
    seats: int
    seats_free: int
    price: int


class Transport(BaseModel):
    point_from: str = Field()
    point_to: str = Field()
    type: str = Field()
    departure: datetime = Field()
    arrival: datetime = Field()
    duration: int = Field()
    price: int = Field()

class Response(BaseModel):
    message: str
    body: List[str]


class Point(BaseModel):
    name: str

