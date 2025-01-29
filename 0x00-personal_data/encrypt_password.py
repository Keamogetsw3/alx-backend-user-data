#!/usr/bin/env python3
"""
This script defines functions for hashing passwords and verifying password validity.
The `hash_password` function returns a securely hashed version of a given password,
while the `is_valid` function checks if a given password matches a stored hashed password.
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """
    Hashes the provided password using bcrypt and returns the hashed result.

    Args:
        password (str): The plain-text password to be hashed.

    Returns:
        bytes: The hashed version of the provided password.

    The password is first encoded into bytes, and then bcrypt's `gensalt()` is used 
    to generate a salt before hashing the password with `hashpw()`.
    """
    # Encode the password into bytes for hashing
    b = password.encode()
    
    # Generate the hashed password using bcrypt
    hashed = hashpw(b, bcrypt.gensalt())
    
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    Verifies if the provided password matches the stored hashed password.

    Args:
        hashed_password (bytes): The stored hashed password.
        password (str): The plain-text password to verify against the hashed password.

    Returns:
        bool: True if the password matches the hashed password, False otherwise.

    The bcrypt `checkpw()` function is used to safely compare the plain-text password 
    with the hashed password, ensuring that sensitive information is not exposed.
    """
    # Compare the provided password with the stored hashed password
    return bcrypt.checkpw(password.encode(), hashed_password)
