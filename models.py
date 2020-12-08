from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class Request(BaseModel):
    date: datetime = Field(
        datetime.now(),
        alias='date',
        title='дата поездки',
        # description='дата для поиска подходящих по дню рейсов'
    )
    arrival: str = Field(
        None,
        alias='arrival-city',
        title='пункт прибытия',
        description='строка с названием пункта прибытия',
        max_length=255
    )
    departure: str = Field(
        None,
        alias='departure-city',
        title='пункт прибытия',
        description='строка с названием пункта прибытия',
        max_length=255
    )


# class Path(BaseModel):
#     point_from: str = Field(
#         title='пункт отправления',
#         max_length=255
#     )
#     point_to: str = Field(
#         title='пункт назаначения',
#         max_length=255
#     )
#     type: str = Field(
#         title='тип транспорта',
#         max_length=255
#     )
#     departure: datetime = Field(
#         title='время отправления'
#     )
#     arrival: datetime = Field(
#         title='время прибытия'
#     )
#     duration: int = Field(
#         title='длительность'
#     )
#     price: int = Field(
#         title='стоимость'
#     )
#
#
# class Response(BaseModel):
#     message: str
#     body: str
