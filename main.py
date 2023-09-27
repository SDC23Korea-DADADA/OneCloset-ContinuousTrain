from fastapi import FastAPI, BackgroundTasks
import logging
import time

from schemas.TrainRequestModel import TrainRequestModel
from service.additional_train_service import save_user_data, additional_train

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# 로그 설정
logger = logging.getLogger(__name__)


@app.post("/additional/train")
async def index(request: TrainRequestModel, background_tasks: BackgroundTasks):
    logger.info(f"[요청 데이터] {request}")
    isSaved = save_user_data(request)
    logger.info(f"[저장 여부] {isSaved}")
    if isSaved is False:
        return {"message": "이미 저장한 clothesId 입니다."}
    else:
        background_tasks.add_task(additional_train)

    return {"message": "요청 정보 저장 성공, 학습 진행시작"}
