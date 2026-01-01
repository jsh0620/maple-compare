import os
import requests
from flask import Flask, render_template

app = Flask(__name__)

API_KEY = os.getenv("NEXON_API_KEY")
HEADERS = {
    "x-nxopen-api-key": API_KEY
}

CHARACTERS = ["란도좀", "키네시스"]

def get_character_data(name):
    # 1️⃣ ocid 조회
    ocid_url = f"https://open.api.nexon.com/maplestory/v1/id?character_name={name}"
    ocid_res = requests.get(ocid_url, headers=HEADERS).json()
    ocid = ocid_res["ocid"]

    # 2️⃣ basic 정보 조회
    basic_url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}"
    basic_res = requests.get(basic_url, headers=HEADERS).json()

    level = int(basic_res["character_level"])
    exp_rate = float(basic_res["character_exp_rate"])  # ⭐ 핵심 수정

    return {
        "name": name,
        "level": level,
        "exp_rate": exp_rate
    }

@app.route("/")
def index():
    data = []

    for name in CHARACTERS:
        data.append(get_character_data(name))

    # ✅ 레벨 → 경험치 내림차순 정렬
    data.sort(
        key=lambda x: (x["level"], x["exp_rate"]),
        reverse=True
    )

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
