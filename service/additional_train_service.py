import os
import requests
import logging
import uuid
import pandas as pd
import subprocess

from datetime import datetime

# 이미지 및 라벨 저장 경로
base_directory = os.path.join(os.path.abspath(os.sep), "home", "j-j9s006", "datasets", "user_additional_dataset")
label_directory = os.path.join(os.path.abspath(os.sep), "home", "j-j9s006", "datasets", "label_dataset")

# 실행 파일 경로
execute_directory = os.path.join(os.path.abspath(os.sep), "home", "j-j9s006", "addtional_train")
execute_file = "additional_train.ipynb"

# 로그 설정
logger = logging.getLogger(__name__)

# 라벨 변환 정보
material_int_to_labels = {
    0: "코듀로이",
    1: "면",
    2: "니트",
    3: "데님",
    4: "시폰",
    5: "패딩",
    6: "트위드",
    7: "플리스",
    8: "가죽",
}

material_labels_to_int = {
    "코듀로이": 0,
    "면": 1,
    "니트": 2,
    "데님": 3,
    "시폰": 4,
    "패딩": 5,
    "트위드": 6,
    "플리스": 7,
    "가죽": 8,
}


def save_user_data(request):
    # for debug
    logger.info(f"[요청 데이터] {request}")

    # 추가 학습을 위한 초기 설정
    additional_train_init()

    # label csv 파일 읽어오기
    df = pd.read_csv(os.path.join(label_directory, "additional_material_label.csv"), encoding='cp949')

    for cloth in request.clothesUrl:
        # 추가학습할 이미지 파일 이름 생성
        fname = str(uuid.uuid4())[:13].replace("-", "") + ".png"

        # 이미지 저장
        save_image(os.path.join(base_directory, fname), cloth.url)

        # label 데이터 추가
        new_row = {"file": fname, "type_id": material_labels_to_int.get(cloth.material),
                   "Filepath": os.path.join(base_directory, fname)}
        df.loc[len(df)] = new_row

    df.to_csv(os.path.join(label_directory, "additional_material_label.csv"), index=False, encoding='cp949')


def additional_train():
    subprocess.run(["jupyter", "nbconvert",
                    "--to", "notebook",
                    "--execute", os.path.join(execute_directory, execute_file),
                    "--output",
                    f"additional_train_{get_current_time()}.ipynb",
                    "--debug"])


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


def additional_train_init():
    # 이미지를 저장할 경로가 없으면 생성
    create_directory(base_directory)
    create_directory(label_directory)
    create_directory(execute_directory)

    # label csv 파일이 없을경우 빈 파일 생성
    if not os.path.exists(os.path.join(label_directory, "additional_material_label.csv")):
        df = pd.DataFrame(columns=["file", "type_id", "Filepath"])
        df.to_csv(os.path.join(label_directory, "additional_material_label.csv"), index=False, encoding='cp949')
