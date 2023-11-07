import subprocess


def run_python_poetry(path: str = "./backend/", filename: str = "run.py"):
    # Run your program
    subprocess.run(["poetry", "run", "python", filename], check=True, cwd=path)
