# dynamic_inventory.py
import subprocess
import json

# Run Terraform output command to get the public IP
terraform_output = subprocess.run(["terraform", "output", "-json"], stdout=subprocess.PIPE, text=True)
output_json = json.loads(terraform_output.stdout)
print(output_json)
# Get the public IP address
public_ip = output_json.get("public_ip", "")
print("this is the public_ip = ", public_ip["value"])
# Generate Ansible inventory
inventory_content = f"[app_servers]\n{public_ip['value']} ansible_ssh_private_key_file=./doodle_key.pem ansible_ssh_user=ubuntu\n"

# Write the inventory to a file
with open("inventory.ini", "w") as inventory_file:
    inventory_file.write(inventory_content)
