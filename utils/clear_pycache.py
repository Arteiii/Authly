import os
import shutil


def clear_pycache(root_dir):
    for root, dirs, files in os.walk(root_dir):
        for d in dirs:
            if d == "__pycache__":
                pycache_dir = os.path.join(root, d)
                shutil.rmtree(pycache_dir)
                print(f"Deleted {pycache_dir}")


clear_pycache("./backend")
