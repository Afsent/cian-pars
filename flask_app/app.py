import joblib
from flask import Flask, render_template
from flask import request
import json
import prepare_data
import numpy as np
import xgboost as xgb
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "xgb.joblib"
SCALE_PATH = "scale.joblib"
SCALE_TARGET_PATH = "scale_target.joblib"

with open(MODEL_PATH, "rb") as fid:
    model = joblib.load(fid)

with open(SCALE_PATH, "rb") as file:
    scale = joblib.load(file)

with open(SCALE_TARGET_PATH, "rb") as file:
    scale_target = joblib.load(file)


@app.route('/')
def index():
    return render_template("index.html",
                           title='Home')


@app.route('/generate', methods=['POST'])
def generate():
    raw_data = request.form
    data = [
        int(raw_data[column])
        for column in ["square", "floor", "floors"]
    ]

    address, subway = raw_data['address'], raw_data['subway']

    lat, lon  = prepare_data.house_geo(address) # получение координат дома
    data.extend([lat, lon])
    data.append(prepare_data.center_distance(address)) # рассчет расстояния до центра
    data.append(prepare_data.subway_distance(address, subway)) # расчет расстояния до метро
    data.append(prepare_data.azimute(lon, lat)) # вычисление азимута

    df = pd.DataFrame([data], columns=labels)
    pred = model.predict(scale.transform([data]))
    predicted = scale_target.inverse_transform(pred)
    price = round(predicted[0]*data[0], 2)
    response = json.dumps({'predicted price per square meter': str(predicted[0]),
                            'predicted price': str(price)
                })
    return response


if __name__ == '__main__':
    app.run()
