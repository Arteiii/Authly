from utils import startup, install_dependencies

path: str = "./backend/"
filename: str = "run.py"

if __name__ == "__main__":
    # Install dependencies
    install_dependencies.poetry(path)

    # Modify the config file
    # modify_config_file()

    # Run the program
    startup.run_python_poetry(path, filename)
