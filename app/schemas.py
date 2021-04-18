from typing import List
from datetime import datetime
from pydantic import BaseModel, validator

# d = {
#     "time": "08.03.2021   13:45:49",
#     "measurement": [
#         {"type": "T", "place": "k\\u00f6niz_bureau", "value": 23.25},
#         {"type": "T", "place": "capi4_CPU", "value": 40.9},
#     ],
# }


class MeasurementBase(BaseModel):
    type: str
    value: float
    place: str


class Measurement(MeasurementBase):
    id: int

    class Config:
        orm_mode = True


class RecordBase(BaseModel):
    time: datetime
    measurement: List[MeasurementBase]

    @validator("time", pre=True)
    def parse_time(cls, v):
        if isinstance(v, str):
            try:
                return datetime.strptime(v, "%d.%m.%Y %H:%M:%S")
            except ValueError:
                pass
        return v


class Record(RecordBase):
    id: int
    time_sync: datetime
    measurement: List[Measurement]

    class Config:
        orm_mode = True
