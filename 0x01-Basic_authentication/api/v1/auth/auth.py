#!/usr/bin/env python3
""" Module manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required for the given path.
        Returns: False
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Return the authorization header from the Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return the current user
        """
        return None
