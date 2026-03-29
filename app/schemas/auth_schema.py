REGISTER_SCHEMA = {
    "type": "object",
    "required": ["email", "password"],
    "properties": {
        "email": {"type": "string", "example": "admin@example.com"},
        "password": {"type": "string", "example": "123456"}
    }
}

LOGIN_SCHEMA = {
    "type": "object",
    "required": ["email", "password"],
    "properties": {
        "email": {"type": "string", "example": "admin@example.com"},
        "password": {"type": "string", "example": "123456"}
    }
}