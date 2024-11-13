#!/usr/bin/env python3
"""
Basic Authentication Module for an API.

Classes:
    BasicAuth: Provides methods to extract and validate user credentials 
               for Basic HTTP authentication.

Imports:
    re: Used for regular expression matching to extract credentials.
    base64: Used to decode Base64-encoded data.
    binascii: Handles Base64 decoding errors.
    typing: Provides type hinting for method signatures.
"""
from .auth import Auth
from models.user import User
import re
import base64
import binascii
from typing import Tuple, TypeVar

class BasicAuth(Auth):
    """
    Basic Authentication Class.

    Methods:
        extract_base64_authorization_header: Extracts the Base64 part of 
            the Authorization header for Basic Authentication
        decode_base64_authorization_header: Decodes a Base64-encoded 
            authorization header
        extract_user_credentials: Extracts the user email and password 
            from a decoded Base64 authorization header
        user_object_from_credentials: Retrieves the User object based on 
            provided email and password
        current_user: Retrieves the authenticated User object from the 
            request, if credentials are valid
    """
    
    def extract_base64_authorization_header(
            self,
            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization header for Basic Authentication.
        
        Args:
            authorization_header (str): The full Authorization header.

        Returns:
            str: The Base64 encoded token from the Authorization header, or None if invalid.
        """
        if type(authorization_header) == str:
            pattern = r'Basic (?P<token>.+)'
            field_match = re.fullmatch(pattern, authorization_header.strip())
            if field_match is not None:
                return field_match.group('token')
        return None

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str) -> str:
        """
        Decodes a Base64-encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded string.

        Returns:
            str: The decoded string in UTF-8 format, or None if decoding fails.
        """
        if type(base64_authorization_header) == str:
            try:
                res = base64.b64decode(
                    base64_authorization_header,
                    validate=True,
                )
                return res.decode('utf-8')
            except (binascii.Error, UnicodeDecodeError):
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str) -> Tuple[str, str]:
        """
        Extracts user credentials from a Base64-decoded authorization header.

        Args:
            decoded_base64_authorization_header (str): Decoded authorization string.

        Returns:
            Tuple[str, str]: A tuple containing the user email and password, 
                             or (None, None) if extraction fails.
        """
        if type(decoded_base64_authorization_header) == str:
            pattern = r'(?P<user>[^:]+):(?P<password>.+)'
            field_match = re.fullmatch(
                pattern,
                decoded_base64_authorization_header.strip(),
            )
            if field_match is not None:
                user = field_match.group('user')
                password = field_match.group('password')
                return user, password
        return None, None

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a user based on the user's authentication credentials.

        Args:
            user_email (str): The user's email.
            user_pwd (str): The user's password.

        Returns:
            User: A User instance if credentials are valid, or None if invalid.
        """
        if type(user_email) == str and type(user_pwd) == str:
            try:
                users = User.search({'email': user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            if users[0].is_valid_password(user_pwd):
                return users[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the user associated with the current request.

        Args:
            request (Any): The request object, typically containing the authorization header.

        Returns:
            User: A User instance if authentication is successful, or None if unsuccessful.
        """
        auth_header = self.authorization_header(request)
        b64_auth_token = self.extract_base64_authorization_header(auth_header)
        auth_token = self.decode_base64_authorization_header(b64_auth_token)
        email, password = self.extract_user_credentials(auth_token)
        return self.user_object_from_credentials(email, password)
