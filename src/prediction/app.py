import os
from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd

app = Flask(__name__)

import pathlib

# Chemin absolu (au format propre pour URI)
# model_path = pathlib.Path(
#     "C:/Users/mlkou/Desktop/devopsMops/src/training/mlruns/972736457168744898/models/m-4162962d358a469485e363fb4ff86cbd/artifacts"
# ).as_posix()

# model = mlflow.pyfunc.load_model(model_uri=f"file:///{model_path}")

import os

model_path = os.path.abspath("mlruns/model")
model = mlflow.pyfunc.load_model(model_uri=f"file://{model_path}")




@app.route("/")
def home():
    return "🏠 API House Price Prediction is running!"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        df = pd.DataFrame([data])
        prediction = model.predict(df)
        return jsonify({"prediction": float(prediction[0])})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
