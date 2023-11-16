import pytest
from authly.core.hashing import Hasher, Bcrypt, Argon, HashingAlgorithmTypes


@pytest.fixture
def password():
    return "test_password"


def test_bcrypt_password_hashing_and_verification(password):
    bcrypt_hash = Hasher.get_password_hash(
        password=password, algorithm=HashingAlgorithmTypes.BCRYPT
    )

    assert Bcrypt.verify_password(bytes(bcrypt_hash), password)  # type: ignore


def test_argon_password_hashing_and_verification(password):
    argon_hash = Hasher.get_password_hash(
        password=password, algorithm=HashingAlgorithmTypes.ARGON2
    )

    assert Argon.verify_password(password, argon_hash)


def test_hasher_verify_password_with_bcrypt(password):
    bcrypt_hash = Hasher.get_password_hash(
        password=password, algorithm=HashingAlgorithmTypes.BCRYPT
    )

    assert Hasher.verify_password(
        password=password,
        stored_hash=bcrypt_hash,
        algorithm=HashingAlgorithmTypes.BCRYPT,
    )


def test_hasher_verify_password_with_argon(password):
    argon_hash = Hasher.get_password_hash(
        password=password, algorithm=HashingAlgorithmTypes.ARGON2
    )

    assert Hasher.verify_password(
        password=password,
        stored_hash=argon_hash,
        algorithm=HashingAlgorithmTypes.ARGON2,
    )


def test_invalid_algorithm_raises_value_error(password):
    with pytest.raises(ValueError):
        Hasher.verify_password(
            password=password,
            stored_hash="some_hash",
            algorithm="invalid_algorithm",
        )
