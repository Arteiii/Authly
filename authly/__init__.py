import importlib
import os


def check_dependencies(dependencies: list):
    for dependency in dependencies:
        try:
            importlib.import_module(dependency)
        except ImportError:
            raise ImportError(
                f"The dependency {dependency} "
                "is not installed or not reachable."
            )
        print(f"{dependency}")


def print_logo(col, reset, file_path: str = "../ascii_art.txt"):
    with open(file_path, "r") as file:
        ascii_art = file.read()
        print(f"{col}{ascii_art}{reset}")


def main():
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

    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    check_dependencies(dependencies_to_check)

    from colorama import Fore, Style

    print("\033c", end="")  # clear screen

    print(os.path.join(base_path, "ascii_art.txt"))

    print_logo(Fore.MAGENTA, Style.RESET_ALL, f"{base_path}/ascii_art.txt")


main()
