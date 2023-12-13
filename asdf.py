import boto3
import subprocess
import json
import time
# def wait_for_instance_init(instance_id, region):
#     ec2_client = boto3.client("ec2", region_name=region)

#     print("Waiting for EC2 instance to be initialized...")

#     while True:
#         response = ec2_client.describe_instance_status(InstanceIds=[instance_id])
#         if response["InstanceStatuses"]:
#             instance_status = response["InstanceStatuses"][0]["InstanceStatus"]["Status"]
#             if instance_status == "ok":
#                 print("EC2 instance is initialized.")
#                 break
#         time.sleep(10)

if __name__ == "__main__":
    terraform_output = subprocess.run(["terraform", "output", "-json"], stdout=subprocess.PIPE, text=True)
    output_json = json.loads(terraform_output.stdout)
    print(output_json)
    # Get the public IP address
    instance_id = output_json.get("instance_id", "")
    region = output_json.get("region", "")
    public_ip = output_json.get("public_ip", "")
    print("this is the public_ip =",public_ip["value"])
    print("this is the instance_id =", instance_id["value"])
    print("this is the region =", region["value"])

    ec2_client = boto3.client("ec2", region_name=region["value"])
    response = ec2_client.describe_instance_status(InstanceIds=[instance_id["value"]])
    print(response)
    instance_status = response["InstanceStatuses"][0]["InstanceStatus"]["Status"]
    print(instance_status)
    time.sleep(3)
    print("its working")