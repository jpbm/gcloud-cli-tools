import sys
from src.util import list_instances, check_instance_exists, retry_command_until_success


def start_instance(name):
    retry_command_until_success(name, "stop")


def main(name):
    instances = list_instances()
    check_instance_exists(instances, name)
    print(f"Trying to stop instance {name}...")
    start_instance(name)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python stop-instance.py <INSTANCE_NAME>")
        sys.exit(1)

    instance_name = sys.argv[1]
    try:
        main(instance_name)
    except ValueError as e:
        print(e)
        sys.exit(1)
