import subprocess
import sys
import time
import re


def list_instances():
    """
    List all available Google Cloud instances using the gcloud command line tool.

    Returns:
        str: A string representation of the list of instances.

    Raises:
        subprocess.CalledProcessError: If there is an error during the
        gcloud command execution.
    """
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
    """
    Check if a specific instance exists in the list of instances.

    Args:
        instances (str): A string representation of the list of instances.
        name (str): The name of the instance to check.

    Raises:
        ValueError: If the instance does not exist in the list.
    """
    if name not in instances:
        raise ValueError(f"No Instance {name} exists.")


def get_instance_property(name, property):
    """
    Get a specific property of a Google Cloud instance.

    Args:
        name (str): The name of the instance.
        property (str): The property to retrieve.

    Returns:
        str: The value of the specified property.

    Raises:
        subprocess.CalledProcessError: If there is an error during
        the gcloud command execution.
    """
    result = subprocess.run(
        ["gcloud", "compute", "instances", "describe", name],
        capture_output=True,
        text=True,
        check=True,
    )
    regex = f"(?<={property}:\s)([\d\.]+)"  # noqa w605
    match = re.search(regex, result.stdout)
    return match.group(0)


def get_instance_ip(name):
    """
    Get the external IP address of a Google Cloud instance.

    Args:
        name (str): The name of the instance.

    Returns:
        str: The external IP address of the instance.
    """
    return get_instance_property(name, "natIP")


def retry_command_until_success(name, command):
    """
    Retry a gcloud command on a specific instance until it succeeds.

    Args:
        name (str): The name of the instance.
        command (str): The gcloud command to execute on the instance.

    Prints:
        Status messages indicating success or failure of the command execution.

    Note:
        This function will prompt the user to enter their GCloud account password.
    """
    print("You may be prompted to enter your GCloud account password (same as email).")
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
