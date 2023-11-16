import pytest
from authly.core import hashing


@pytest.fixture
def password():
    return "test_password"


def test_argon_password_hashing_and_verification(password):
    argon_hash = hashing.get_password_hash(password)

    assert hashing.verify_password(password, argon_hash)


def test_hasher_verify_password_with_argon(password):
    argon_hash = hashing.get_password_hash(password=password)

    assert hashing.verify_password(
        password=password,
        stored_hash=argon_hash,
    )
