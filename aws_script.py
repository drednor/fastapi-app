# dynamic_inventory.py
import subprocess
import json
import boto3
import time
import os
import sys


def run_terraform():
    current_script_directory = os.path.dirname(os.path.abspath(__file__))

    print("Current working directory:", os.getcwd())
    try:
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform", "apply", "-auto-approve"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Terraform execution failed: {e}")
        exit(1)
    # Run Terraform output command to get the public IP
    terraform_output = subprocess.run(["terraform", "output"], cwd=current_script_directory, stdout=subprocess.PIPE)
    print(terraform_output)
    decoded_output = terraform_output.stdout.decode('utf-8')
    print(decoded_output)
    lines = decoded_output.split('\n')
    output_dict = {}
    for line in lines:
        print(line)
        if line:
            parts = line.split('=')
            if len(parts) == 2:
                key, value = map(str.strip, parts)
                output_dict[key] = value.strip('\"')
    print(output_dict['instance_id'])
    print(output_dict['region'])
    print(output_dict['public_ip'])
    # Generate Ansible inventory
    inventory_content = f"[app_servers]\n{output_dict['public_ip']} ansible_ssh_private_key_file=./doodle_key.pem ansible_ssh_user=ubuntu\n"
    # Write the inventory to a file
    with open("inventory.ini", "w") as inventory_file:
        inventory_file.write(inventory_content)
        
    return output_dict['public_ip'], output_dict['region'], output_dict['instance_id']


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


def destroy_terraform():
    try:
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform","destroy","-auto-approve"],check=True)
    except subprocess.CalledProcessError as e:
        print(f"terraform destroy failed - {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "deploy":
            public_ip, region, instance_id = run_terraform()
            wait_for_initialization(instance_id, region)
            run_ansible()
            print("Deployment Done")
        elif sys.argv[1] == "destroy":
            destroy_terraform()
            print("ec2 Instance Destroyed")
    print("done")
    





