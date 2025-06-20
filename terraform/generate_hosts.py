import json
import subprocess

def get_instance_ips():
    result = subprocess.run(["tofu", "output", "-json"], capture_output=True, text=True)
    outputs = json.loads(result.stdout)
    return outputs["api_public_ip"]["value"], outputs["training_public_ip"]["value"]

def write_ansible_hosts(api_ip, training_ip):
    content = f"""[api]
{api_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem

[training]
{training_ip} ansible_user=ubuntu ansible_ssh_private_key_file=~/.ssh/vockey.pem
"""
    with open("../ansible/hosts", "w") as f:
        f.write(content)
    print("✅ Fichier Ansible 'hosts' mis à jour.")

if __name__ == "__main__":
    api_ip, training_ip = get_instance_ips()
    write_ansible_hosts(api_ip, training_ip)
