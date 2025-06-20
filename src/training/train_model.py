import pandas as pd
import mlflow
import mlflow.xgboost
import xgboost as xgb
from sklearn.metrics import mean_squared_error
from math import sqrt
import os
import shutil

# Définir les chemins vers les données
base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
data_path_X = os.path.join(base_dir, "data/processed/X_train.csv")
data_path_y = os.path.join(base_dir, "data/processed/y_train.csv")

# Chargement des données
X = pd.read_csv(data_path_X)
y = pd.read_csv(data_path_y)

# Exemple d'entrée (utile pour l'API ou signature MLflow)
input_example = X.iloc[[0]]

# Pas besoin de tracking distant ici, on sauvegarde localement
mlflow.set_experiment("house-price-prediction")

with mlflow.start_run():
    model = xgb.XGBRegressor(n_estimators=100, max_depth=4, learning_rate=0.1, random_state=42)
    model.fit(X, y)

    preds = model.predict(X)
    rmse = sqrt(mean_squared_error(y, preds))
    mlflow.log_metric("rmse", rmse)

    # ✅ Supprimer le dossier modèle s’il existe déjà
    model_dir = "model"
    if os.path.exists(model_dir):
        shutil.rmtree(model_dir)

    # ✅ Sauvegarde locale
    mlflow.xgboost.save_model(
        model,
        path=model_dir,
        input_example=input_example
    )

    print(f"📦 Modèle XGBoost sauvegardé localement avec RMSE = {rmse:.2f}")
