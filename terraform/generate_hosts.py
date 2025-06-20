import json
import subprocess
import shutil
import sys
import os

def find_tofu_executable():
    tofu_path = shutil.which("tofu")
    if tofu_path:
        return tofu_path
    else:
        # Cas spécifique Windows : chercher dans AppData
        possible_path = os.path.expandvars(r"%LocalAppData%\tofu\bin\tofu.exe")
        if os.path.exists(possible_path):
            return possible_path
        raise FileNotFoundError("❌ L'exécutable 'tofu' est introuvable. Vérifie qu'il est installé et présent dans le PATH.")

def get_instance_ips(tofu_cmd):
    result = subprocess.run([tofu_cmd, "output", "-json"], capture_output=True, text=True)
    outputs = json.loads(result.stdout)
    return outputs["api_public_ip"]["value"], outputs["training_public_ip"]["value"]

def write_ansible_hosts(api_ip, training_ip):
    content = f"""[api]
{api_ip} ansible_user=ubuntu ansible_ssh_private_key_file=../_credentials/vockey.pem

[training]
{training_ip} ansible_user=ubuntu ansible_ssh_private_key_file=../_credentials/vockey.pem
"""
    with open("../ansible/hosts", "w") as f:
        f.write(content)
    print("✅ Fichier Ansible 'hosts' mis à jour avec succès.")

if __name__ == "__main__":
    try:
        tofu_path = find_tofu_executable()
        api_ip, training_ip = get_instance_ips(tofu_path)
        write_ansible_hosts(api_ip, training_ip)
    except Exception as e:
        print(f"❌ Erreur : {e}")
        sys.exit(1)
