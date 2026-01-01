from flask import Flask, render_template
import requests
import os

app = Flask(__name__)

API_KEY = os.environ.get("NEXON_API_KEY")
HEADERS = {
    "x-nxopen-api-key": API_KEY
}

CHARACTERS = ["란도좀", "키ne네시s"]

def get_ocid(name):
    url = f"https://open.api.nexon.com/maplestory/v1/id?character_name={name}"
    return requests.get(url, headers=HEADERS).json()["ocid"]

def get_basic_info(ocid):
    url = f"https://open.api.nexon.com/maplestory/v1/character/basic?ocid={ocid}"
    return requests.get(url, headers=HEADERS).json()

@app.route("/")
def index():
    data = []

    for name in CHARACTERS:
        ocid = get_ocid(name)
        basic = get_basic_info(ocid)

        data.append({
            "name": name,
            "level": basic["character_level"],
            "exp_rate": basic["character_exp_rate"]
        })

    data.sort(key=lambda x: (x["level"], x["exp_rate"]), reverse=True)

    return render_template("index.html", characters=data)

# ⭐ Render 필수
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
