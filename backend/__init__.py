import importlib
import os
import logging
from datetime import datetime


def check_dependencies():
    dependencies_to_check = [
        "colorama",
        "fastapi",
        "motor",
        "bcrypt",
        "argon2",
        "uvicorn",
        "redis",
        "exrex",
    ]

    for dependency in dependencies_to_check:
        try:
            importlib.import_module(dependency)
        except ImportError:
            raise ImportError(
                f"The dependency {dependency}"
                "is not installed or not reachable."
            )
        logging.info(f"{dependency}")


def print_logo(col, file_path: str = "./ascii_art.txt"):
    try:
        with open(file_path, "r") as file:
            ascii_art = file.read()
            print(f"{col}{ascii_art}")
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def log_basic_config(path, base_path):
    log_directory = os.path.join(base_path, "log")
    os.makedirs(log_directory, exist_ok=True)

    log_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_checks.log"
    log_file_path = os.path.join(log_directory, log_file)

    logging.basicConfig(
        filename=log_file_path,
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return log_file_path


def main():
    module_directory = os.path.dirname(__file__)
    base_path = os.path.dirname(os.path.abspath(__file__))

    log_basic_config(module_directory, base_path=base_path)

    check_dependencies()

    from colorama import Fore

    print("\033c", end="")  # clear screen
    print_logo(Fore.MAGENTA, f"{base_path}/ascii_art.txt")


main()
