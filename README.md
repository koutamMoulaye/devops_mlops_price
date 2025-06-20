# MLOps House Price Prediction Project

## Objectif

Ce projet permet de déployer une API Flask pour la prédiction de prix de maisons via un modèle XGBoost, avec infrastructure provisionnée automatiquement sur AWS via Terraform, et une exécution des tâches de configuration par Ansible.

---
---
le mlflow
![alt text](image.png)
![alt text](image-1.png)
![alt text](image-2.png)
---
## 🌐 Prérequis

### 1. Clés AWS

* crée le  fichier `_credentials/aws_learner_lab_credentials`
* Exemple :

  ```ini
  [awslearnerlab]
  aws_access_key_id = YOUR_ACCESS_KEY_ID
  aws_secret_access_key = YOUR_SECRET_ACCESS_KEY
  ```

### 2. Clé SSH pour EC2

* Placez votre clé SSH privée `labuser.pem` dans le dossier `_credentials/`
* Donnez-lui les bons droits :

  ```bash
  chmod 400 _credentials/labuser.pem
  ```

### 3. Outils requis

Installez les outils suivants :

* [OpenTofu (Terraform fork)](https://opentofu.org/)
* Ansible
* Python 3.10+
* Docker (installé sur l'instance API via Ansible)

---


### 1. Clonez le projet

```bash
git clone https://github.com/koutamMoulaye/devops_mlops_price.git
cd devops_mlops_price
```

### 2. Provisionner l'infrastructure AWS

```bash
cd terraform

# Initialiser OpenTofu
tofu init
tofu plan

# Déployer les ressources
tofu apply
```

### 3. Générer automatiquement les hôtes Ansible

```bash
python generate_hosts.py
```

Ce script met à jour `ansible/hosts` avec les bonnes IP publiques.

### 4. Déployer les services avec Ansible

```bash
cd ../ansible

# Déployer l'API Flask sur l'instance API
ansible-playbook -i hosts playbooks/setup_api.yml

# Lancer l'entraînement du modèle sur l'instance ML
ansible-playbook -i hosts playbooks/setup_ml.yml
```

---

## Utilisation de l'API

Envoyez une requête POST vers l'API Flask avec un JSON d'exemple comme `sample_input.json`.

```powershell
Invoke-RestMethod -Uri http://<API_PUBLIC_IP>:5001/predict `
  -Method Post `
  -ContentType "application/json" `
  -InFile ".\data\processed\sample_input.json"
```

```ubuntu ou kali ou powershell

curl -X POST http://<IP_API>:5001/predict \
     -H "Content-Type: application/json" \
     -d @data/processed/sample_input.json

---

## Arborescence Simplifiée

```
devops_mlops_price/
├── ansible/
│   ├── playbooks/
│   │   ├── setup_api.yml
│   │   └── setup_ml.yml
│   └── hosts
├── terraform/
│   ├── main.tf
│   ├── output.tf
│   └── generate_hosts.py
├── src/
│   ├── prediction/app.py
│   └── training/train_model.py
├── _credentials/
│   ├── aws_learner_lab_credentials
│   └── labuser.pem
```
