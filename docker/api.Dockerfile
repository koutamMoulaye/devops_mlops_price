# docker/api.Dockerfile

FROM python:3.10-slim

RUN apt-get update && apt-get install -y gcc

WORKDIR /app

COPY requirements.txt .
COPY src/prediction ./src/prediction

# Spécifie le chemin exact vers ton modèle (corrigé ici)
COPY src/training/mlruns/972736457168744898/models/m-4162962d358a469485e363fb4ff86cbd/artifacts ./mlruns/model

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5001

CMD ["python", "src/prediction/app.py"]
