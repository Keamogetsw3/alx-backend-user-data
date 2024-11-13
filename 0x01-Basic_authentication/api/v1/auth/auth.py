#!/usr/bin/env python3
""" Module manage the API authentication
"""
from typing import List, TypeVar
from flask import request


class Auth:
     """
    Auth class manage the API authentication
    Methods:
        def require_auth(self, path: str, excluded_paths: List[str]) -> bool: Authenticates a user.
        def authorization_header(self, request=None) -> str: contains authentication
    credentials needed to access protected resources
        def current_user(self, request=None) -> TypeVar('User'): that returns None - request will be the Flask request object
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required for the given path.
        Returns:
            True if the path is not in excluded_paths, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        
        normalized_path = path if path.endswith('/') else path + '/'
        
        if normalized_path in excluded_paths:
            return False
        return True


    def authorization_header(self, request=None) -> str:
        """ Return the authorization header from the Flask request object.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Return the current user
        """
        return None
