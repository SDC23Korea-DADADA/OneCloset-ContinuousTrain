import os
import requests
import logging
import uuid
import pandas as pd

from datetime import datetime

base_directory = os.path.join(os.path.abspath(os.sep), "home", "j-j9s006", "datasets", "user_additional_dataset")
logger = logging.getLogger(__name__)


def additional_train(request):
    # for debug
    logger.info(f"[요청 데이터] {request}")

    create_directory(base_directory)

    for cloth in request.clothesUrl:
        # 추가학습할 이미지 파일 이름 생성
        fname = str(uuid.uuid4())[:13].replace("-", "") + ".png"

        # 이미지 저장
        save_image(os.path.join(base_directory, fname), cloth.url)

        # label csv 데이터 생성


def save_image(save_path, url):
    with requests.get(url) as r:
        if r.status_code == 200:
            logger.info("[Download] " + url + " is completed")
            with open(save_path, 'wb') as f:
                f.write(r.content)
        else:
            logger.error("[Download] " + url + " is failed")


def create_directory(path):
    """
    주어진 경로에 디렉토리를 생성합니다.
    디렉토리가 이미 존재하면 생성하지 않습니다.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")
    else:
        print(f"Directory '{path}' already exists.")


def get_current_time():
    # 현재 시간 가져오기
    current_time = datetime.now()

    # 년월일-시분초 로 포맷지정
    formatted_time = current_time.strftime('%y%m%d-%H%M%S')

    return formatted_time
