import pytest
from authly.core import password_validation, username_validation


@pytest.mark.parametrize(
    "password, expected_result, expected_message",
    [
        ("1234567", False, "Password must be at least 8 characters long."),
        (
            "passwithoutuppercase",
            False,
            "Password must contain at least one uppercase letter.",
        ),
        (
            "PASSWITHOUTLOWERCASE",
            False,
            "Password must contain at least one lowercase letter.",
        ),
        (
            "PAss@@!!!WITHOutDIGITS",
            False,
            "Password must contain at least one digit.",
        ),
        (
            "P4SSW1TH3V3RYTH1ngbutsp3z14l",
            False,
            "Password must contain at least one special character (@$!%*?&).",
        ),
        ("V3ryS3cureP@Ss", True, "Password matches Requirements"),
        (
            "5aYtH/Mh.O4LQkSqQ?l;h$df%'J]Ex1^qT",
            True,
            "Password matches Requirements",
        ),
    ],
)
def test_password_complexity_validation(
    password, expected_result, expected_message
):
    result, message = password_validation.validate_password_complexity(
        password
    )
    assert result == expected_result
    assert message == expected_message


def test_short_password():
    short_password = "Short!"
    result, message = password_validation.validate_password_complexity(
        short_password
    )
    assert result is False
    assert "Password must be at least 8 characters long." in message


@pytest.mark.parametrize(
    "username, expected_result",
    [
        ("abc#1234", True),
        ("xyz#5678", True),
        ("abc1234", False),
        ("12#abcd", False),
        ("abc#12345", False),
    ],
)
def test_username_validation(username, expected_result):
    result = username_validation.validate_username(username)
    assert result == expected_result
