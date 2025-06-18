import pandas as pd
import mlflow
import mlflow.xgboost
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from math import sqrt
import os

# Définir les chemins vers les données
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
data_path_X = os.path.join(base_dir, "data/processed/X_train.csv")
data_path_y = os.path.join(base_dir, "data/processed/y_train.csv")

# Chargement des données
X = pd.read_csv(data_path_X)
y = pd.read_csv(data_path_y)

# Exemple d'entrée (utile pour l'API ou signature MLflow)
input_example = X.iloc[[0]]

# Définir l'expérience MLflow
mlflow.set_experiment("house-price-prediction")

with mlflow.start_run():
    # Création du modèle XGBoost
    model = xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X, y)

    # Évaluation
    preds = model.predict(X)
    rmse = sqrt(mean_squared_error(y, preds))
    mlflow.log_metric("rmse", rmse)

    # Enregistrement du modèle dans MLflow
    mlflow.xgboost.log_model(
        model,
        artifact_path="model",
        registered_model_name="HousePriceModel",
        input_example=input_example
    )

    print(f"📦 Modèle XGBoost loggé avec RMSE = {rmse:.2f}")
