import subprocess
import sys
import time


def list_instances():
    try:
        result = subprocess.run(
            ["gcloud", "compute", "instances", "list"],
            capture_output=True,
            text=True,
            check=True,
        )
        instances = result.stdout.strip()
        print("Available instances:\n", instances)
        return instances
    except subprocess.CalledProcessError as e:
        print("Error listing instances:", e.stderr)
        sys.exit(1)


def check_instance_exists(instances, name):
    if name not in instances:
        raise ValueError(f"No Instance {name} exists.")


def retry_command_until_success(name, command):
    print(f"You may be prompted to enter your GCloud account password (same as email).")
    while True:
        try:
            _ = subprocess.run(
                ["gcloud", "compute", "instances", command, name],
                capture_output=True,
                text=True,
                check=True,
            )
            print(f"Command {command} ran successfully on Instance {name}.")
            break
        except subprocess.CalledProcessError as e:
            print(f"Error on command {command} instance {name}: {e.stderr}")
            for i in range(5):
                print(f"Retrying in {5-i} seconds...", end="\r")
                time.sleep(1)
            print(f"Retrying in {0} seconds...", end="\n")
