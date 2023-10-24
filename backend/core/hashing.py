import bcrypt
import argon2

from core.config import config

argon_config = config.PasswordConfig.ArgonHashingAlgorithm
bcrypt_config = config.PasswordConfig.BcryptHashingAlgorithm


class Bcrypt:
    """
    A class for handling password hashing and verification using Bcrypt.
    """

    @staticmethod
    def verify_password(stored_hash, password):
        """
        Verify a password against a stored Bcrypt hash.

        Args:
            stored_hash (bytes): The stored Bcrypt hash.
            password (str): The password to be verified.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        return bcrypt.checkpw(
            password.encode(bcrypt_config.ENCODING),
            stored_hash,
        )

    @staticmethod
    def get_password_hash(password):
        """
        Hash a password using Bcrypt.

        Args:
            password (str): The password to be hashed.

        Returns:
            bytes: The Bcrypt hash of the password.
        """
        salt = bcrypt.gensalt(rounds=bcrypt_config.ROUNDS)
        hashed_password = bcrypt.hashpw(
            password.encode(bcrypt_config.ENCODING),
            salt,
        )
        return hashed_password


class Argon:
    """
    A class for handling password hashing and verification using Argon2.
    """

    @staticmethod
    def verify_password(password, stored_hash):
        """
        Verify a password against a stored Argon2 hash.

        Args:
            password (str): The password to be verified.
            stored_hash (str): The stored Argon2 hash.

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        try:
            hasher = argon2.PasswordHasher(
                time_cost=argon_config.TIME_COST,
                memory_cost=argon_config.MEMORY_COST,
                parallelism=argon_config.PARALLELISM,
                hash_len=argon_config.HASH_LEN,
                salt_len=argon_config.SALT_LEN,
                encoding=argon_config.ENCODING,
            )
            return hasher.verify(stored_hash, password)
        except argon2.exceptions.VerifyMismatchError:
            return False

    @staticmethod
    def get_password_hash(password):
        """
        Hash a password using Argon2.

        Args:
            password (str): The password to be hashed.

        Returns:
            str: The Argon2 hash of the password.
        """
        hasher = argon2.PasswordHasher(
            time_cost=config.argon_config.TIME_COST,
            memory_cost=config.argon_config.MEMORY_COST,
            parallelism=config.argon_config.PARALLELISM,
            hash_len=config.argon_config.HASH_LEN,
            salt_len=config.argon_config.SALT_LEN,
            encoding=config.argon_config.ENCODING,
        )
        return hasher.hash(password)


class Hasher:
    """
    A class for handling password hashing and
    verification using various algorithms.
    """

    @staticmethod
    def verify_password(
        password,
        stored_hash,
        algorithm=config.PasswordConfig.HASHING_ALGORITHM,
    ):
        """
        Verify a password against a stored hash\
            using the specified hashing algorithm.

        Args:
            password (str): The password to be verified.
            stored_hash (str): The stored hash.
            algorithm (str): The hashing algorithm to use\
                (either "bcrypt" or "argon2").

        Returns:
            bool: True if the password is valid, False otherwise.
        """
        if algorithm == "bcrypt":
            return Bcrypt.verify_password(stored_hash, password)
        elif algorithm == "argon2":
            return Argon.verify_password(password, stored_hash)
        else:
            raise ValueError("Invalid hashing algorithm")

    @staticmethod
    def get_password_hash(
        password,
        algorithm=config.PasswordConfig.HASHING_ALGORITHM,
    ):
        """
        Hash a password using the specified hashing algorithm.

        Args:
            password (str): The password to be hashed.
            algorithm (str): The hashing algorithm to use\
                (either "bcrypt" or "argon2").

        Returns:
            str: The hash of the password.
        """
        if algorithm == "bcrypt":
            return Bcrypt.get_password_hash(password)
        elif algorithm == "argon2":
            return Argon.get_password_hash(password)
        else:
            raise ValueError("Invalid hashing algorithm")


if __name__ == "__main__":
    if input("compare hash with pw?").lower().startswith("y"):
        password = input("enter password:")
        hash = input("enter hash:")
        if input("use Bcrypt?").lower().startswith("y"):
            print(
                Hasher.verify_password(
                    password=password, stored_hash=hash, algorithm="bcrypt"
                )
            )

        print(
            Hasher.verify_password(
                password=password, stored_hash=hash, algorithm="argon2"
            )
        )

    password = input("enter password:")
    if input("use Bcrypt?").lower().startswith("y"):
        print(Hasher.get_password_hash(password=password, algorithm="bcrypt"))

    print(Hasher.get_password_hash(password=password, algorithm="argon2"))
