import os


def list_files_in_subfolder(subfolder_path):
    file_list = []
    for root, dirs, files in os.walk(subfolder_path):
        for file in files:
            file_list.append(os.path.join(root, file))
    return file_list


subfolder_path = "./backend/"
file_list = list_files_in_subfolder(subfolder_path)
print(file_list)
