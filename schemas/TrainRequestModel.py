from typing import List
from pydantic import BaseModel


class ClothesInfo(BaseModel):
    clothesId: str
    type: str
    material: str
    url: str


class TrainRequestModel(BaseModel):
    clothesUrl: List[ClothesInfo]
