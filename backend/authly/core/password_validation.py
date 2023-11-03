"""
Password Complexity Validation Module

This module provides a function to validate the complexity of a password based\
    on specific requirements, such as minimum length, uppercase letters,\
        lowercase letters, digits, and special characters.

Author: Arteii
Date: 24/10/2023

Usage:
    from validate_password_complexity import validate_password_complexity

    try:
        validated_password = validate_password_complexity("Passw0rd!")
        print(f"Valid password: {validated_password}")
    except ValueError as e:
        print(f"Invalid password: {e}")

The `validate_password_complexity` function checks if a given password meets\
the specified complexity requirements. In this example,\
    the requirements include:
- A minimum length of 8 characters.
- At least one uppercase letter.
- At least one lowercase letter.
- At least one digit.
- At least one special character from the set: @, $, !, %, *, ?, &.

Example:
    Valid: "Passw0rd!", "S@feP@ss"
    Invalid: "12345678", "Password", "special!"
"""


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
