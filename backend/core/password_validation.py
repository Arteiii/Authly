import re


def validate_password_complexity(password: str):
    # Define your complexity requirements using regular expressions
    # In this example, the password must have at least one uppercase letter,
    # one lowercase letter, one digit, and one special character.

    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters long.")

    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain at least one uppercase letter."
        )

    if not re.search(r"[a-z]", password):
        raise ValueError(
            "Password must contain at least one lowercase letter."
        )

    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")

    if not re.search(r"[@$!%*?&]", password):
        raise ValueError(
            "Password must contain at least one special character (@$!%*?&)."
        )

    return password
