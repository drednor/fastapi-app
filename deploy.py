# dynamic_inventory.py
import subprocess
import json
import boto3
import time


def run_terraform():
    current_script_directory = os.path.dirname(os.path.abspath(__file__))
    terraform_directory = os.path.join(current_script_directory, 'path', 'to', 'your', 'terraform', 'directory')
    try:
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Terraform execution failed: {e}")
        exit(1)
    # Run Terraform output command to get the public IP
    terraform_output = subprocess.run(["terraform", "output", "-json"], stdout=subprocess.PIPE, text=True, cwd=terraform_directory)
    output_json = json.loads(terraform_output.stdout)
    if terraform_output.returncode != 0:
        print("Error running Terraform command:")
        print("STDOUT:", terraform_output.stdout)
        print("STDERR:", terraform_output.stderr)
        exit(1)
    print(output_json)
    # Get the public IP address
    instance_id = output_json.get("instance_id", "")
    region = output_json.get("region", "")
    public_ip = output_json.get("public_ip", "")
    print("this is the public_ip =",public_ip["value"])
    print("this is the instance_id =", instance_id["value"])
    print("this is the region =", region["value"])
    # Generate Ansible inventory
    inventory_content = f"[app_servers]\n{public_ip['value']} ansible_ssh_private_key_file=./doodle_key.pem ansible_ssh_user=ubuntu\n"
    # Write the inventory to a file
    with open("inventory.ini", "w") as inventory_file:
        inventory_file.write(inventory_content)

    return public_ip["value"], region["value"], instance_id["value"]


def wait_for_initialization(instance_id, region):
    ec2_client = boto3.client("ec2", region_name=region)
    print("Waiting for EC2 instance to be initialized...")

    while True:
        response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
        if response["InstanceStatuses"]:
            instance_status = response["InstanceStatuses"][0]["InstanceStatus"]["Status"]
            print("current instance status =",instance_status)
            if instance_status == "ok":
                print("EC2 instance is initialized.")
                break
        time.sleep(30)

def run_ansible():
    command = "ANSIBLE_HOST_KEY_CHECKING=False ansible-playbook -i inventory.ini ansible_playbook.yml"
    try:
        subprocess.run(command,shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"error Ansible {e}")

if __name__ == "__main__":
    public_ip, region, instance_id = run_terraform()
    wait_for_initialization(instance_id, region)
    run_ansible()





