import subprocess

def destroy_terraform():
    try:
        subprocess.run(["terraform", "init"], check=True)
        subprocess.run(["terraform","destroy","-auto-approve"],check=True)
    except subprocess.CalledProcessError as e:
        print(f"terraform destroy failed - {e}")

if __name__ == "__main__":
    destroy_terraform()
    print("ec2 Instance Destroyed")