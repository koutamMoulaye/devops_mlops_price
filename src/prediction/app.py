from flask import Flask, request, jsonify
import mlflow.pyfunc
import pandas as pd
from pathlib import Path

app = Flask(__name__)

# Charge le modèle depuis le chemin local dans l'image Docker
model_path = Path("mlruns/model").resolve().as_uri()
model = mlflow.pyfunc.load_model(model_path)

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
