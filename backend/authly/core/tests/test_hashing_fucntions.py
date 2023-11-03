from authly.core.hashing import Hasher


def test_argon_hashing() -> None:
    hashed = Hasher.get_password_hash(algorithm="argon2", password="Test123")
    result = Hasher.verify_password(
        algorithm="argon2", stored_hash=hashed, password="Test123"
    )
    assert result is True


def test_bcrypt_hashing() -> None:
    hashed = Hasher.get_password_hash(algorithm="bcrypt", password="Test123")
    result = Hasher.verify_password(
        algorithm="bcrypt", stored_hash=hashed, password="Test123"
    )
    assert result is True
