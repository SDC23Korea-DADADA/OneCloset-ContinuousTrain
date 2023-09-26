import fastapi
import logging

from schemas.TrainRequestModel import TrainRequestModel
from service.additional_train_service import additional_train

app = fastapi.FastAPI()
logging.basicConfig(level=logging.INFO)


@app.get("/additional/train")
async def index(request: TrainRequestModel):
    additional_train(request)
    return {"message": "Hello, FastAPI!"}

