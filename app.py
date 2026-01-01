import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

# Render / 로컬 공통 환경변수
API_KEY = os.getenv("NEXON_API_KEY")

HEADERS = {
    "x-nxopen-api-key": API_KEY
}

# 고정 캐릭터
CHARACTERS = ["런도좀", "키ne네시s", "Nerix", "먹은탐켄치"]


def get_character_data(name):
    # 1️⃣ OCID 조회
    ocid_url = (
        "https://open.api.nexon.com/maplestory/v1/id"
        f"?character_name={name}"
    )
    ocid_res = requests.get(ocid_url, headers=HEADERS).json()

    if "ocid" not in ocid_res:
        print("OCID ERROR:", ocid_res)
        return None

    ocid = ocid_res["ocid"]

    # 2️⃣ BASIC 정보 조회 (레벨 + 경험치)
    basic_url = (
        "https://open.api.nexon.com/maplestory/v1/character/basic"
        f"?ocid={ocid}"
    )
    basic_res = requests.get(basic_url, headers=HEADERS).json()

    if "character_level" not in basic_res:
        print("BASIC API ERROR:", basic_res)
        return None

    return {
        "name": name,
        "level": int(basic_res["character_level"]),
        # 🔥 정렬 핵심: float으로 저장
        "exp_rate": float(basic_res["character_exp_rate"])
    }


@app.route("/")
def index():
    data = []

    for name in CHARACTERS:
        char = get_character_data(name)
        if char:
            data.append(char)

    # ✅ 레벨 → 경험치 퍼센트 기준 내림차순
    data.sort(
        key=lambda x: (x["level"], x["exp_rate"]),
        reverse=True
    )

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
