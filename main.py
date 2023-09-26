from fastapi import FastAPI, BackgroundTasks
import logging
import time

from schemas.TrainRequestModel import TrainRequestModel
from service.additional_train_service import save_user_data, additional_train

app = FastAPI()
logging.basicConfig(level=logging.INFO)


@app.post("/additional/train")
async def index(request: TrainRequestModel, background_tasks: BackgroundTasks):
    save_user_data(request)
    background_tasks.add_task(additional_train)
    return {"message": "요청 정보 저장 성공, 학습 진행시작"}
