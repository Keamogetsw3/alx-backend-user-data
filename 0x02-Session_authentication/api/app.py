#!/usr/bin/env python3
"""
This module sets up and configures the API routes for the application.
It includes route definitions, error handlers, and authentication setup.
"""

from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import CORS, cross_origin
import os

# Initialize the Flask application
app = Flask(__name__)
# Register the blueprint for the API routes
app.register_blueprint(app_views)

# Enable Cross-Origin Resource Sharing (CORS) for the API
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the auth variable and choose the authentication method based on environment variable
auth = None
AUTH_TYPE = os.getenv("AUTH_TYPE")

# Set the authentication type based on the environment variable
if AUTH_TYPE == "auth":
    from api.v1.auth.auth import Auth
    auth = Auth()
elif AUTH_TYPE == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif AUTH_TYPE == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
elif AUTH_TYPE == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth
    auth = SessionExpAuth()
elif AUTH_TYPE == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth
    auth = SessionDBAuth()

# Filter request before it's passed to the route handler
@app.before_request
def bef_req():
    """
    This function is executed before each request.
    It checks authentication and applies authorization logic.
    """
    if auth is None:
        # If no authentication method is configured, skip this check
        pass
    else:
        # Attach the current_user to the request object if authentication is set
        setattr(request, "current_user", auth.current_user(request))
        excluded = [
            '/api/v1/status/',  # Health check endpoint
            '/api/v1/unauthorized/',  # Unauthorized error page
            '/api/v1/forbidden/',  # Forbidden error page
            '/api/v1/auth_session/login/'  # Login endpoint that doesn't require authorization
        ]
        # Check if the path requires authentication
        if auth.require_auth(request.path, excluded):
            cookie = auth.session_cookie(request)
            # If no authorization header or session cookie is provided, return 401
            if auth.authorization_header(request) is None and cookie is None:
                abort(401, description="Unauthorized")
            # If the current user is not found, return 403 (Forbidden)
            if auth.current_user(request) is None:
                abort(403, description="Forbidden")

# Define custom error handler for 404 - Not Found
@app.errorhandler(404)
def not_found(error) -> str:
    """
    Handler for 404 errors (page not found).
    """
    return jsonify({"error": "Not found"}), 404

# Define custom error handler for 401 - Unauthorized
@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    Handler for 401 errors (unauthorized access).
    """
    return jsonify({"error": "Unauthorized"}), 401

# Define custom error handler for 403 - Forbidden
@app.errorhandler(403)
def forbidden(error) -> str:
    """
    Handler for 403 errors (forbidden access).
    """
    return jsonify({"error": "Forbidden"}), 403

# Run the application
if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")  # Default to all interfaces
    port = getenv("API_PORT", "5000")  # Default to port 5000
    app.run(host=host, port=port)
