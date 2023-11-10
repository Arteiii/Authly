from pathlib import Path


def clean_pycache(directory: str):
    deleted_directories = []

    for path in Path(directory).rglob("__pycache__"):
        if path.is_dir():
            path.rmdir()
            deleted_directories.append(str(path))
            print(f"Deleted {deleted_directories}")


if __name__ == "__main__":
    clean_pycache("./backend")
