import importlib
import subprocess
import time


def check_and_install_dependencies():
    try:
        # Check if Poetry is installed
        subprocess.run(
            ["poetry", "--version"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        print("Poetry is installed.")

        # Run poetry install
        subprocess.run(["poetry", "install"], check=True)
        print("Dependencies installed successfully.")
    except subprocess.CalledProcessError:
        print(
            "Error: Poetry is not installed or there was an "
            "issue installing dependencies."
        )


def check_dependencies(dependencies: list):
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            return False
    return True


def main():
    dependencies_to_check = [
        "requests",
    ]

    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        if check_dependencies(dependencies_to_check):
            print("All dependencies are satisfied.")
            break
        else:
            print("Some dependencies are missing. Attempting to install...")
            check_and_install_dependencies()
            time.sleep(2)  # Optional: Wait for a few seconds before rechecking
            attempts += 1
    else:
        print("Max attempts reached. Aborting.")


main()
