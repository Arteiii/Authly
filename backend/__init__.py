import importlib
import os
import subprocess


def install_dependencies(module_directory):
    os.chdir(module_directory)

    # Install dependencies using Poetry
    subprocess.run(["poetry", "install"], check=True)


module_directory = os.path.dirname(__file__)

install_dependencies(module_directory)


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
                f"The dependency {dependency}"
                f"is not installed or not reachable."
            )
        print(dependency)


def check_python_files():
    required_files = [
        "./__init__.py",
        "./authly/app.py",
        "./authly/__init__.py",
        "./authly/api/api_router.py",
        "./authly/api/__init__.py",
        "./authly/api/api_v1/api.py",
        "./authly/api/api_v1/__init__.py",
        "./authly/api/api_v1/authentication/token.py",
        "./authly/api/api_v1/authentication/user_authorization.py",
        "./authly/api/api_v1/authentication/__init__.py",
        "./authly/api/api_v1/key/api.py",
        "./authly/api/api_v1/key/generation.py",
        "./authly/api/api_v1/key/managment.py",
        "./authly/api/api_v1/key/model.py",
        "./authly/api/api_v1/key/__init__.py",
        "./authly/api/api_v1/user/managment.py",
        "./authly/api/api_v1/user/model.py",
        "./authly/api/api_v1/user/user.py",
        "./authly/api/api_v1/user/__init__.py",
        "./authly/config_temp/config.json",
        "./authly/core/config.py",
        "./authly/core/converter.py",
        "./authly/core/hashing.py",
        "./authly/core/log.py",
        "./authly/core/object_id.py",
        "./authly/core/password_validation.py",
        "./authly/core/username_validation.py",
        "./authly/core/__init__.py",
        "./authly/core/db/mongo.py",
        "./authly/core/db/redis.py",
        "./authly/core/db/__init__.py",
        "./authly/core/status/mongo_test.py",
        "./authly/core/status/redis_test.py",
        "./authly/core/status/__init__.py",
        "./authly/core/tests/test_hashing_fucntions.py",
        "./authly/core/tests/__init__.py",
    ]

    for file_path in required_files:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} is missing.")
        print(file_path)


# Perform checks
check_dependencies()
check_python_files()
