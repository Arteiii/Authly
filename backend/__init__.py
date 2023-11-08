import importlib
import hashlib
import os
import subprocess
import json
import shutil
import logging
from datetime import datetime


base_path = os.path.dirname(os.path.abspath(__file__))


def clear_console():
    os.system("cls" if os.name == "nt" else "clear")


def get_subfiles(directory_path):
    subfiles = []
    for root, dirs, files in os.walk(directory_path):
        for name in files:
            subfiles.append(
                os.path.relpath(os.path.join(root, name), base_path)
            )
    return subfiles


def clean_pycache(directory):
    """
    Clean all __pycache__ directories in the specified directory.
    """
    deleted_directories = []
    for root, dirs, _ in os.walk(directory):
        for d in dirs:
            if d == "__pycache__":
                pycache_path = os.path.join(root, d)
                shutil.rmtree(pycache_path)
                deleted_directories.append(pycache_path)
    return deleted_directories


def install_dependencies(module_directory):
    os.chdir(module_directory)

    # Install dependencies using Poetry
    subprocess.run(["poetry", "install"], check=True)


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


def check_new_files(directory, expected_hashes):
    """
    Check for new files in the directory and
    prompt the user to add their hashes.
    """
    new_files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            filepath = os.path.relpath(os.path.join(root, filename), base_path)
            if filepath not in expected_hashes:
                new_files.append(filepath)
    return new_files


def remove_missing_files(expected_files):
    missing_files = [
        file_path
        for file_path in expected_files
        if not os.path.exists(os.path.join(base_path, file_path))
    ]
    if missing_files:
        print("Missing files found:")
        for f in missing_files:
            print(f)

        user_input = input(
            "Do you want to remove all missing files from the expected files?"
            "(y/n): "
        )
        if user_input.lower() == "y":
            for f in missing_files:
                expected_files.pop(f, None)
                logging.info(f"Removed {f} from expected files")
        else:
            print("Skipping removal of missing files.")


def check_existing_files(expected_files):
    """
    Check existing files against their expected hashes.
    """
    for filepath, expected_hash in expected_files.items():
        full_path = os.path.join(base_path, filepath)
        if os.path.exists(full_path):
            with open(full_path, "rb") as file:
                file_hash = hashlib.sha256(file.read()).hexdigest()
                if file_hash != expected_hash:
                    print(
                        f"{Fore.YELLOW}Hash mismatch{Style.RESET_ALL}"
                        f"{Fore.YELLOW}for {filepath}{Style.RESET_ALL}. "
                    )
                    user_input = input(
                        "Do you want to update the hash? (y/n): "
                    )
                    if user_input.lower() == "y":
                        expected_files[filepath] = file_hash
                        logging.info
                        print(f"Hash updated for {filepath}.")
                    else:
                        logging.info(f"Skipping {filepath} hash update")
                        print(f"Skipping {filepath} hash update.")
                else:
                    logging.info(f"Hash match for: {filepath}")
                    print(
                        f"{Fore.GREEN}Hash match for "
                        f"{Fore.GREEN}{filepath}{Style.RESET_ALL}."
                    )
        else:
            logging.error(f"File {filepath} does not exist.")
            print(
                f"{Fore.RED}File {filepath} does not exist.{Style.RESET_ALL}"
            )


def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(os.path.join(base_path, file_path), "rb") as file:
        content = file.read()
        hasher.update(content)
    return hasher.hexdigest()


############################################################
#                         setup                            #
############################################################

log_directory = os.path.join(base_path, "log")
os.makedirs(log_directory, exist_ok=True)

log_file = datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_checks.log"
log_file_path = os.path.join(log_directory, log_file)


logging.basicConfig(
    filename=log_file_path,
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


module_directory = os.path.dirname(__file__)

install_dependencies(module_directory)

check_dependencies()


from colorama import Fore, Style


directory_path = os.path.join(base_path, "authly")


############################################################
#                      clean pycache                       #
############################################################

cleaned_directories = clean_pycache(directory_path)
print(f"{Fore.BLUE}Deleted pycache directories:{Style.RESET_ALL}")
for d in cleaned_directories:
    logging.info(f"Removed: {d}")
    print(f"{Fore.RED}{d}{Style.RESET_ALL}")


############################################################
#               get subfiles & compare hash                #
############################################################


subfiles = get_subfiles(directory_path)

if os.path.exists(os.path.join(base_path, "hashes.json")):
    with open(os.path.join(base_path, "hashes.json"), "r") as file:
        expected_files = json.load(file)
else:
    logging.error("hashes.json not found")
    expected_files = {}

new_files = check_new_files(directory_path, expected_files)
if new_files:
    print("New files found:")
    for f in new_files:
        logging.info(f"new file: {f}")
        print(f)

    user_input = input(
        "Do you want to add all new files to expected files? (a/n): "
    )
    if user_input.lower() == "a":
        logging.info(f"user added all new files ({user_input})")
        for f in new_files:
            file_hash = get_file_hash(f)
            expected_files[f] = file_hash
            logging.info(f"Added {f} with hash {file_hash} to expected files")
            print(f"Added {f} with hash {file_hash} to expected files.")
    else:
        for f in new_files:
            user_input = input(
                f"Do you want to add {f} to expected files? (y/n): "
            )
            if user_input.lower() == "y":
                file_hash = get_file_hash(f)
                expected_files[f] = file_hash
                logging.info(
                    f"Added {f} with hash {file_hash} to expected files"
                )
                print(f"Added {f} with hash {file_hash} to expected files.")

check_existing_files(expected_files)

remove_missing_files(expected_files)

with open("hashes.json", "w") as file:
    json.dump(expected_files, file, indent=4)

print("\n")

clear_console()
print(
    Fore.MAGENTA,
    r"""
 ______           __    __       ___
/\  _  \         /\ \__/\ \     /\_ \
\ \ \L\ \  __  __\ \ ,_\ \ \___ \//\ \    __  __
 \ \  __ \/\ \/\ \\ \ \/\ \  _ `\ \ \ \  /\ \/\ \
  \ \ \/\ \ \ \_\ \\ \ \_\ \ \ \ \ \_\ \_\ \ \_\ \
   \ \_\ \_\ \____/ \ \__\\ \_\ \_\/\____\\/`____ \
    \/_/\/_/\/___/   \/__/ \/_/\/_/\/____/ `/___/> \
                                              /\___/
                                              \/__/
    """,
    Fore.RESET,
)

print(f"{Fore.BLUE}check: {log_file_path} for details{Fore.RESET}\n \n")
