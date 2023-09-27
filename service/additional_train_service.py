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
material_file = "additional_material_train.ipynb"
type_file = "additional_type_train.ipynb"

# 로그 설정
logger = logging.getLogger(__name__)

# 라벨 변환 정보
material_int_to_labels = {
    0: "코듀로이", 1: "면", 2: "니트", 3: "데님",
    4: "시폰", 5: "패딩", 6: "트위드", 7: "플리스", 8: "가죽",
}

material_labels_to_int = {
    "코듀로이": 0, "면": 1, "니트": 2, "데님": 3,
    "시폰": 4, "패딩": 5, "트위드": 6, "플리스": 7, "가죽": 8,
}

# 종류 라벨 변환 정보
type_labels_to_int = {'긴팔티': 0, '반팔티': 1, '셔츠/블라우스': 2, '니트웨어': 3, '후드티': 4, '민소매': 5,
                      '긴바지': 6, '반바지': 7, '롱스커트': 8, '미니스커트': 9,
                      '코트': 10, '재킷': 11, '점퍼/짚업': 12, '패딩': 13, '가디건': 14, '베스트': 15,
                      '원피스': 16, '점프수트': 17}
type_int_to_labels = {0: '긴팔티', 1: '반팔티', 2: '셔츠/블라우스', 3: '니트웨어', 4: '후드티', 5: '민소매',
                      6: '긴바지', 7: '반바지', 8: '롱스커트', 9: '미니스커트',
                      10: '코트', 11: '재킷', 12: '점퍼/짚업', 13: '패딩', 14: '가디건', 15: '베스트',
                      16: '원피스', 17: '점프수트'}


def save_user_data(request):
    # for debug
    logger.info(f"[요청 데이터] {request}")

    # 추가 학습을 위한 초기 설정
    additional_train_init()

    # label csv 파일 읽어오기
    material_df = pd.read_csv(os.path.join(label_directory, "additional_material_label.csv"), encoding='cp949')
    type_df = pd.read_csv(os.path.join(label_directory, "additional_type_label.csv"), encoding='cp949')

    # clothes csv 읽어오기
    clothes_df = pd.read_csv(os.path.join(label_directory, "additional_clothesId.csv"), encoding='cp949')
    clothes_id_set = set(clothes_df['clothesId'])
    clothes_id_set = {str(element) for element in clothes_id_set}
    logger.info(f"[clothesId] {clothes_id_set}")

    for cloth in request.clothesUrl:
        # 기존 저장되어 있는 clothesId 인지 확인
        if cloth.clothesId in clothes_id_set:
            logger.info(f"[clothesId] {cloth.clothesId} is already saved")
            return False

        # clothes id 추가
        new_clothes_id = {"clothesId": cloth.clothesId, "time": get_current_time()}
        clothes_df.loc[len(clothes_df)] = new_clothes_id


        # 추가학습할 이미지 파일 이름 생성
        fname = str(uuid.uuid4())[:13].replace("-", "") + ".png"

        # 이미지 저장
        save_image(os.path.join(base_directory, fname), cloth.url)

        # 학습데이터 validation 수행
        image_validation(os.path.join(base_directory, fname), cloth.material, cloth.type)

        # material label 데이터 추가
        material_new_row = {"file": fname, "type_id": material_labels_to_int.get(cloth.material),
                            "Filepath": os.path.join(base_directory, fname)}
        material_df.loc[len(material_df)] = material_new_row

        # type label 데이터 추가
        type_new_row = {"file_name": fname, "type": type_labels_to_int.get(cloth.type),
                        "file_path": os.path.join(base_directory, fname)}
        type_df.loc[len(type_df)] = type_new_row

    material_df.to_csv(os.path.join(label_directory, "additional_material_label.csv"), index=False, encoding='cp949')
    type_df.to_csv(os.path.join(label_directory, "additional_type_label.csv"), index=False, encoding='cp949')
    clothes_df.to_csv(os.path.join(label_directory, "additional_clothesId.csv"), index=False, encoding='cp949')


def additional_train():
    logger.info("[Train] Start additional train")
    subprocess.run(["jupyter", "nbconvert",
                    "--to", "notebook",
                    "--execute", os.path.join(execute_directory, material_file),
                    "--output",
                    f"./ipynb_material_output/additional_material_train_{get_current_time()}.ipynb",
                    "--debug"])
    subprocess.run(["jupyter", "nbconvert",
                    "--to", "notebook",
                    "--execute", os.path.join(execute_directory, type_file),
                    "--output",
                    f"./ipynb_type_output/additional_type_train_{get_current_time()}.ipynb",
                    "--debug"])
    logger.info("[Train] End additional train")


def image_validation(image_path, material, type):
    # TODO: 사용자가 입력한 이미지에 대한 검증 작업 로직
    #  검증결과 학습 데이터로 사용이 가능하다면 True, 불가능하다면 False 반환
    return True


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

    # material label csv 파일이 없을경우 빈 파일 생성
    if not os.path.exists(os.path.join(label_directory, "additional_material_label.csv")):
        df = pd.DataFrame(columns=["file", "type_id", "Filepath"])
        df.to_csv(os.path.join(label_directory, "additional_material_label.csv"), index=False, encoding='cp949')

    # type label csv 파일이 없을경우 빈 파일 생성
    if not os.path.exists(os.path.join(label_directory, "additional_type_label.csv")):
        df = pd.DataFrame(columns=["file_name", "type", "file_path"])
        df.to_csv(os.path.join(label_directory, "additional_type_label.csv"), index=False, encoding='cp949')

    # clothesId csv 파일이 없을경우 빈 파일 생성
    if not os.path.exists(os.path.join(label_directory, "additional_clothesId.csv")):
        df = pd.DataFrame(columns=["clothesId"])
        df.to_csv(os.path.join(label_directory, "additional_clothesId.csv"), index=False, encoding='cp949')
