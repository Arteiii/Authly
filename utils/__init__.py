import importlib
import os


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
        "./backend/.gitignore",
        "./backend/poetry.lock",
        "./backend/pyproject.toml",
        "./backend/README.md",
        "./backend/requirements.txt",
        "./backend/__init__.py",
        "./backend/authly/app.py",
        "./backend/authly/__init__.py",
        "./backend/authly/api/api_router.py",
        "./backend/authly/api/__init__.py",
        "./backend/authly/api/api_v1/api.py",
        "./backend/authly/api/api_v1/__init__.py",
        "./backend/authly/api/api_v1/authentication/token.py",
        "./backend/authly/api/api_v1/authentication/user_authorization.py",
        "./backend/authly/api/api_v1/authentication/__init__.py",
        "./backend/authly/api/api_v1/key/api.py",
        "./backend/authly/api/api_v1/key/generation.py",
        "./backend/authly/api/api_v1/key/managment.py",
        "./backend/authly/api/api_v1/key/model.py",
        "./backend/authly/api/api_v1/key/__init__.py",
        "./backend/authly/api/api_v1/user/managment.py",
        "./backend/authly/api/api_v1/user/model.py",
        "./backend/authly/api/api_v1/user/user.py",
        "./backend/authly/api/api_v1/user/__init__.py",
        "./backend/authly/config_temp/config.json",
        "./backend/authly/core/config.py",
        "./backend/authly/core/converter.py",
        "./backend/authly/core/hashing.py",
        "./backend/authly/core/log.py",
        "./backend/authly/core/object_id.py",
        "./backend/authly/core/password_validation.py",
        "./backend/authly/core/username_validation.py",
        "./backend/authly/core/__init__.py",
        "./backend/authly/core/db/mongo.py",
        "./backend/authly/core/db/redis.py",
        "./backend/authly/core/db/__init__.py",
        "./backend/authly/core/status/mongo_test.py",
        "./backend/authly/core/status/redis_test.py",
        "./backend/authly/core/status/__init__.py",
        "./backend/authly/core/tests/test_hashing_fucntions.py",
        "./backend/authly/core/tests/__init__.py",
    ]  # Update with your required Python files

    for file_path in required_files:
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"The file {file_path} is missing.")
        print(file_path)


# Perform checks
check_dependencies()
check_python_files()
