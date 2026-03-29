import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret-key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key-that-is-at-least-32-characters-long")
    JWT_SECRET_KEY = "this_is_a_very_long_secure_secret_key_123456"

    SWAGGER = {
        "title": "Airline Ticketing API",
        "uiversion": 3
    }