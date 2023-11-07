import subprocess


def poetry(path: str = "./backend/"):
    subprocess.run(["poetry", "install"], check=True, cwd=path)
