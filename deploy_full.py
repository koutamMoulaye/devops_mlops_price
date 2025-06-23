import os
import subprocess
import json
import time

# === CONFIGURATION ===
CREDENTIALS_PEM_SRC = "_credentials/vockey.pem"
CREDENTIALS_PEM_DST = os.path.expanduser("~/.ssh/vockey.pem")
ANSIBLE_HOSTS_PATH = "ansible/hosts"
API_PLAYBOOK = "playbooks/setup_api.yml"
ML_PLAYBOOK = "playbooks/setup_ml.yml"
TOFU_DIR = "terraform"


def run_command(cmd, cwd=None, capture=False):
    print(f"\n🚀 Executing: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True)
    if result.returncode != 0:
        print(f"❌ Error: {' '.join(cmd)}")
        if capture:
            print(result.stderr)
        exit(1)
    return result.stdout.strip() if capture else None


def init_and_apply_terraform():
    os.chdir(TOFU_DIR)
    run_command(["tofu", "init"])
    run_command(["tofu", "apply", "-auto-approve"])
    output = run_command(["tofu", "output", "-json"], capture=True)
    os.chdir("..")
    return json.loads(output)


def setup_ssh_key():
    print("\n🔐 Configuration de la clé SSH")
    os.makedirs(os.path.expanduser("~/.ssh"), exist_ok=True)
    run_command(["sudo", "cp", CREDENTIALS_PEM_SRC, CREDENTIALS_PEM_DST])
    run_command(["sudo", "chmod", "400", CREDENTIALS_PEM_DST])


def generate_ansible_hosts(api_ip, ml_ip):
    content = f"""[api]
{api_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem

[training]
{ml_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem
"""
    with open(ANSIBLE_HOSTS_PATH, "w") as f:
        f.write(content)
    print("✅ Fichier Ansible hosts mis à jour")


def test_api(ip):
    print("\n🧪 Test de l'API Flask...")
    for attempt in range(12):  # Jusqu'à 60 sec
        try:
            response = subprocess.check_output([
                "curl", "-s", "-X", "POST",
                f"http://{ip}:5001/predict",
                "-H", "Content-Type: application/json",
                "-d", "@data/processed/sample_input.json"
            ])
            print(f"📡 Réponse API : {response.decode('utf-8')}")
            return True
        except subprocess.CalledProcessError:
            print(f"⌛ Tentative {attempt + 1}/12 : API non encore disponible. Nouvelle tentative dans 5 sec...")
            time.sleep(5)
    print("❌ L'API n'a pas répondu après 60 secondes.")
    return False


if __name__ == "__main__":
    print("\n📦 Déploiement complet en cours...")
    output = init_and_apply_terraform()

    api_ip = output["api_public_ip"]["value"]
    ml_ip = output["training_public_ip"]["value"]

    setup_ssh_key()
    generate_ansible_hosts(api_ip, ml_ip)

    print("\n⚙️  Déploiement de l'API...")
    run_command(["ansible-playbook", "-i", "hosts", API_PLAYBOOK], cwd="ansible")

    if test_api(api_ip):
        proceed = input("\n✅ API OK. Voulez-vous continuer avec l'entraînement ML ? (y/n): ")
        if proceed.lower() == 'y' or 'yes':
            print("\n⚙️  Déploiement du training ML...")
            run_command(["ansible-playbook", "-i", "hosts", ML_PLAYBOOK], cwd="ansible")
        else:
            print("⏭ Entraînement ignoré.")
    else:
        print("❌ L'API n'est pas accessible. Arrêt du processus.")
