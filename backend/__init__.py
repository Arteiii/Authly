import importlib
import hashlib
import os
import subprocess
import json
import shutil

base_path = os.path.dirname(os.path.abspath(__file__))


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
    for root, dirs, _ in os.walk(directory):
        for d in dirs:
            if d == "__pycache__":
                pycache_path = os.path.join(root, d)
                shutil.rmtree(pycache_path)


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
                f"The dependency {dependency} is not installed or not reachable."
            )
        print(dependency)


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
                    user_input = input(
                        f"Hash mismatch for {filepath}. "
                        "Do you want to update the hash? (y/n): "
                    )
                    if user_input.lower() == "y":
                        expected_files[filepath] = file_hash
                        print(f"Hash updated for {filepath}.")
                    else:
                        print(f"Skipping {filepath} hash update.")
                else:
                    print(f"Hash match for {filepath}.")
        else:
            print(f"File {filepath} does not exist.")


def get_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(os.path.join(base_path, file_path), "rb") as file:
        content = file.read()
        hasher.update(content)
    return hasher.hexdigest()


############################################################
#                     validate authly                      #
############################################################

module_directory = os.path.dirname(__file__)

install_dependencies(module_directory)

check_dependencies()

directory_path = os.path.join(base_path, "authly")

print(f"working directory: {directory_path}")

clean_pycache(directory_path)
print("__pycache__ directories cleaned")

subfiles = get_subfiles(directory_path)
for f in subfiles:
    print(f)


if os.path.exists(os.path.join(base_path, "hashes.json")):
    with open(os.path.join(base_path, "hashes.json"), "r") as file:
        expected_files = json.load(file)
else:
    expected_files = {}

new_files = check_new_files(directory_path, expected_files)
if new_files:
    print("New files found:")
    for f in new_files:
        print(f)

    user_input = input(
        "Do you want to add all new files to expected files? (a/n): "
    )
    if user_input.lower() == "a":
        for f in new_files:
            file_hash = get_file_hash(f)
            expected_files[f] = file_hash
            print(f"Added {f} with hash {file_hash} to expected files.")
    else:
        for f in new_files:
            user_input = input(
                f"Do you want to add {f} to expected files? (y/n): "
            )
            if user_input.lower() == "y":
                file_hash = get_file_hash(f)
                expected_files[f] = file_hash
                print(f"Added {f} with hash {file_hash} to expected files.")

check_existing_files(expected_files)


with open("hashes.json", "w") as file:
    json.dump(expected_files, file, indent=4)
