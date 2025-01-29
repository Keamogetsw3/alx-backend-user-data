#!/usr/bin/env python3
""" 
Module for handling User views in the API.
This module contains routes for viewing, creating, updating, and deleting users.
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User

# Route to retrieve all users
@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """
    GET /api/v1/users
    Returns:
      - A list of all User objects in JSON format.
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)

# Route to retrieve a single user by ID
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """
    GET /api/v1/users/:id
    Path parameter:
      - user_id: The ID of the user to retrieve.
    Returns:
      - A single User object in JSON format.
      - 404 if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    # Special case for the "me" user ID, representing the currently authenticated user
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    # Retrieve user by ID
    user = User.get(user_id)
    if user is None:
        abort(404)
    if request.current_user is None:
        abort(404)
    return jsonify(user.to_json())

# Route to delete a user by ID
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """
    DELETE /api/v1/users/:id
    Path parameter:
      - user_id: The ID of the user to delete.
    Returns:
      - Empty JSON response if the User is successfully deleted.
      - 404 if the User ID doesn't exist.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()  # Delete the user
    return jsonify({}), 200

# Route to create a new user
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """
    POST /api/v1/users
    JSON body:
      - email: The user's email (required).
      - password: The user's password (required).
      - last_name: The user's last name (optional).
      - first_name: The user's first name (optional).
    Returns:
      - The newly created User object in JSON format.
      - 400 if there are missing required fields or other errors.
    """
    rj = None
    error_msg = None
    try:
        rj = request.get_json()  # Attempt to parse JSON body
    except Exception as e:
        rj = None
    if rj is None:
        error_msg = "Wrong format"  # JSON format error
    # Validate required fields
    if error_msg is None and rj.get("email", "") == "":
        error_msg = "email missing"
    if error_msg is None and rj.get("password", "") == "":
        error_msg = "password missing"
    if error_msg is None:
        try:
            # Create a new user with the provided data
            user = User()
            user.email = rj.get("email")
            user.password = rj.get("password")
            user.first_name = rj.get("first_name")
            user.last_name = rj.get("last_name")
            user.save()  # Save user to the database
            return jsonify(user.to_json()), 201
        except Exception as e:
            error_msg = f"Can't create User: {e}"  # Handle any other creation errors
    return jsonify({'error': error_msg}), 400  # Return error if creation failed

# Route to update an existing user's information
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """
    PUT /api/v1/users/:id
    Path parameter:
      - user_id: The ID of the user to update.
    JSON body:
      - last_name: The user's last name (optional).
      - first_name: The user's first name (optional).
    Returns:
      - The updated User object in JSON format.
      - 404 if the User ID doesn't exist.
      - 400 if the update fails.
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    rj = None
    try:
        rj = request.get_json()  # Attempt to parse JSON body
    except Exception as e:
        rj = None
    if rj is None:
        return jsonify({'error': "Wrong format"}), 400  # Return error if JSON format is invalid
    # Update fields if provided in the request body
    if rj.get('first_name') is not None:
        user.first_name = rj.get('first_name')
    if rj.get('last_name') is not None:
        user.last_name = rj.get('last_name')
    user.save()  # Save updated user data
    return jsonify(user.to_json()), 200
