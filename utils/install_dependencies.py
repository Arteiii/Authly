import subprocess


def poetry(path: str = "./backend/"):
    subprocess.run(["poetry", "install"], check=True, cwd=path, shell=False)


if __name__ == "__main__":
    poetry()
