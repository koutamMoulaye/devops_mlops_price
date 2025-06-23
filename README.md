# MLOps House Price Prediction

## Objectif

Ce projet déploie automatiquement :

- Une API Flask pour la prédiction de prix de maisons (modèle XGBoost)
- Deux instances EC2 (API + Training) via OpenTofu (Terraform)
- La configuration logicielle via Ansible
- Le tout contrôlé par un script `deploy_full.py`

---

##  Prérequis

1. **Clés AWS Learner Lab**

Créez le fichier `_credentials/aws_learner_lab_credentials` :

```ini
[awslearnerlab]
aws_access_key_id = VOTRE_ACCESS_KEY
aws_secret_access_key = VOTRE_SECRET_KEY
```

2. **Clé SSH EC2**

Placez votre clé privée `vockey.pem` dans `_credentials/` :

```bash
chmod 400 _credentials/vockey.pem
```

3. **Outils installés en local**

- Python 3.10+
- [OpenTofu (Terraform)](https://opentofu.org/)
- Ansible
- Docker *(déployé sur l'instance API)*

---

##  Déploiement Automatisé

Lancez tout le processus avec un seul script :

```bash
python3 deploy_full.py
```

Ce script :

1. Crée l'infrastructure AWS
2. Configure la clé SSH et Ansible
3. Déploie l’API avec Docker
4. Vérifie l’API automatiquement
5. Demande confirmation avant d'entraîner le modèle ML

---

##  Tester l'API

Une fois le déploiement terminé :

```bash
curl -X POST http://<API_PUBLIC_IP>:5001/predict \
     -H "Content-Type: application/json" \
     -d @data/processed/sample_input.json
```

> Exemple de réponse :

```json
{"prediction": 206580.66396249738}
```

---

## 🛠 Dépannage Courant

### Problème de permissions .pem

Erreur :

```
UNPROTECTED PRIVATE KEY FILE!
```

 Solution :

```bash
mkdir -p ~/.ssh
cp _credentials/vockey.pem ~/.ssh/vockey.pem
chmod 400 ~/.ssh/vockey.pem
```

### Assurez-vous que `ansible/hosts` pointe vers le bon chemin :

```ini
[api]
<ip_api> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem

[training]
<ip_training> ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem
```

---

##  Résultats Visualisés

### MLflow tracking

<p align="center">
  <img src="image.png" width="600"/>
</p>
<p align="center">
  <img src="image-1.png" width="600"/>
</p>
<p align="center">
  <img src="image-2.png" width="600"/>
</p>

---

## Structure du Projet

```
devops_mlops_price/
├── ansible/
│   ├── playbooks/
│   │   ├── setup_api.yml
│   │   └── setup_ml.yml
│   └── hosts
├── terraform/
│   └── main.tf, output.tf...
├── src/
│   ├── prediction/app.py
│   └── training/train_model.py
├── data/
│   └── processed/sample_input.json
├── _credentials/
│   ├── aws_learner_lab_credentials
│   └── vockey.pem
├── deploy_full.py
├── README.md
└── images...
```

---

## Pour un Déploiement Manuel

Si besoin :

```bash
cd terraform
tofu init && tofu apply

python3 deploy_full.py  # (recommandé)
```