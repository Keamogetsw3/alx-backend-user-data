#!/usr/bin/env python3
"""
Module to manage API authentication.
"""

from typing import List, TypeVar
from flask import request


class Auth:
    """
    Auth class to manage API authentication.

    Methods:
        require_auth(path: str, excluded_paths: List[str]) -> bool:
            Determines if a given path requires authentication.
        authorization_header(request=None) -> str:
            Retrieves the authorization header from the Flask request, if available.
        current_user(request=None) -> TypeVar('User'):
            Retrieves the current authenticated user (returns None by default).
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for the given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): List of paths that do not require authentication.

        Returns:
            bool: True if the path requires authentication, False otherwise.
        """
        if path is None:
            return True
        if not excluded_paths:
            return True
        
        normalized_path = path if path.endswith('/') else path + '/'
        
        return normalized_path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the Flask request object.

        Args:
            request (Flask.request): The Flask request object.

        Returns:
            str: The authorization header if present, None otherwise.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current authenticated user.

        Args:
            request (Flask.request): The Flask request object.

        Returns:
            TypeVar('User'): The current user (None by default).
        """
        return None
