#!/usr/bin/env python3
import bcrypt  # Import the bcrypt library for password hashing


def hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt.

    Args:
        password (str): The plaintext password to be hashed.

    Returns:
        bytes: A salted, hashed password, represented as a byte string.
    """
    # Encode the plaintext password as bytes
    p = password.encode()
    # Generate a salt and hash the password using bcrypt
    return bcrypt.hashpw(p, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Validates a password against its hashed counterpart using bcrypt.

    Args:
        hashed_password (bytes): The previously hashed password.
        password (str): The plaintext password to be validated.

    Returns:
        bool: True if the plaintext password matches the hashed password, False otherwise.
    """
    # Encode the plaintext password as bytes and compare it with the hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)
