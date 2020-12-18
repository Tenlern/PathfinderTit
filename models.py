from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime, date


# Класс для данных запроса к api
class Request(BaseModel):
    d: date = Field(
        "2000-01-01",
        alias='date',
        title='дата поездки',
        description='дата для поиска подходящих по дню рейсов'
    )
    type: str = Field(
        "plane",
        alias='type',
        title='тип траснпорта',
        description='тип транспорта для поиска маршрута plain/bus/train',
        max_length=16
    )
    departure: str = Field(
        None,
        alias='from',
        title='пункт прибытия',
        description='строка с названием пункта прибытия',
        max_length=255
    )
    arrival: str = Field(
        None,
        alias='to',
        title='пункт прибытия',
        description='строка с названием пункта прибытия',
        max_length=255
    )

    class Config:
        schema_extra = {
            "example": {
                "date": "2008-09-15",
                "type": "plain",
                "from": "москва",
                "to": "санкт-петербург",
            }
        }


class Route(BaseModel):
    point_from: str = Field(
        alias="from",
        title='пункт отправления',
        description="начало пути",
        max_length=16
    )
    point_to: str = Field(
        alias="to",
        title='пункт назаначения',
        description="конец пути",
        max_length=16
    )
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
    duration: int = Field(
        alias="duration",
        title='длительность',
        description="длительность поездки"
    )
    price: int = Field(
        alias="price",
        title='стоимость',
        description="стоимость поздки"
    )


class Response(BaseModel):
    message: str
    type: str = Field(
        title='тип транспорта',
        description='тип транспорта',
        max_length=255
    )
    path: List[Route] = Field(
        None,
        alias="path",
        title="маршрут",
        description="вычисленный оптимальный маршурт на основе входящих данных с целью уменьшения длительности поездки"
    )

    class Config:
        schema_extra = {
            "example": {
                "message": "Nice!",
                "type": "plain",
                "path": [
                    {"from": "талин", "to": "рига", "duration": 2257, "price": 4090},
                    {"from": "рига", "to": "москва", "duration": 3487, "price": 8198}
                ]
            },
        }
