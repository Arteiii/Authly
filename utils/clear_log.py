import os


def get_parent_path(path):
    parent_path = os.path.dirname(path)
    return parent_path


def clear_log_files(directory: str) -> None:
    for root, dirs, files in os.walk(directory):
        for dir_name in dirs:
            log_subdirectory = os.path.join(root, dir_name)

            for file_name in os.listdir(log_subdirectory):
                if file_name.endswith(".log"):
                    file_path = os.path.join(log_subdirectory, file_name)

                    try:
                        os.remove(file_path)

                        print(f"Deleted log file: {file_path}")

                    except Exception as e:
                        print(f"Error deleting log file {file_path}: {e}")


if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    paren_directory = get_parent_path(current_path)

    clear_log_files(paren_directory)
