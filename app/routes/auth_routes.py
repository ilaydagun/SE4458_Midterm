from flask import Blueprint, request
from app.services.auth_service import register_user, login_user
from app.utils.helpers import success_response, error_response

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["POST"])
def register():
    """
    Register a new user
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: admin@example.com
            password:
              type: string
              example: 123456
    responses:
      201:
        description: User registered successfully
      400:
        description: Invalid input or user already exists
    """
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response("Email and password are required", 400)

    user, error = register_user(email, password)

    if error:
        return error_response(error, 400)

    return success_response("User registered successfully", user.to_dict(), 201)


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Login user
    ---
    tags:
      - Auth
    consumes:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - email
            - password
          properties:
            email:
              type: string
              example: admin@example.com
            password:
              type: string
              example: 123456
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    data = request.get_json() or {}

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return error_response("Email and password are required", 400)

    result, error = login_user(email, password)

    if error:
        return error_response(error, 401)

    return success_response("Login successful", result, 200)