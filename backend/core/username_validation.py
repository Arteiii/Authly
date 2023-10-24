import re


def validate_username(value: str):
    """
    Validate the username format using a regular expression.

    Args:
        value (str): The username to validate.

    Returns:
        str: The validated username.

    Raises:
        ValueError: If the username format is invalid.
    """
    # Define the regular expression pattern for the username
    pattern = r"^[a-zA-Z]{3,}#[0-9]{4}$"

    if not re.match(pattern, value):
        raise ValueError(
            "Invalid username format. Username must consist of 3 letters,\
                    a '#' character, and 4 numbers. (abc#1234)"
        )

    return value
