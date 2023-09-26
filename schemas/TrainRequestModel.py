from typing import List
from pydantic import BaseModel


class ClothesInfo(BaseModel):
    type: str
    material: str
    url: str


class TrainRequestModel(BaseModel):
    clothesUrl: List[ClothesInfo]
