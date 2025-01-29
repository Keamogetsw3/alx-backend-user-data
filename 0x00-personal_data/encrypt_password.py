#!/usr/bin/env python3
"""
Defines functions to hash passwords and verify validity.
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Hashes the password using bcrypt and returns the hashed result.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        bytes: The hashed password.
    """
    # Encode the password into bytes for hashing
    b = password.encode()
    
    # Generate the hashed password using bcrypt
    hashed = hashpw(b, bcrypt.gensalt())
    
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies if the password matches the hashed password.

    Args:
        hashed_password (bytes): The stored hashed password.
        password (str): The plain-text password to verify.

    Returns:
        bool: True if the password matches, False otherwise.
    """
    # Compare the password with the stored hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)
