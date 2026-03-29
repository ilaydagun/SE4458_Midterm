import os
from flask import Flask
from config import Config
from app.extensions import db, migrate, jwt, swagger, limiter


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    os.makedirs("instance", exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    limiter.init_app(app)
    swagger.init_app(app)

    from app.models import User, Flight, Ticket, CheckIn

    from app.routes.auth_routes import auth_bp
    from app.routes.flight_routes import flight_bp
    from app.routes.ticket_routes import ticket_bp
    from app.routes.checkin_routes import checkin_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(flight_bp, url_prefix="/flights")
    app.register_blueprint(ticket_bp, url_prefix="/tickets")
    app.register_blueprint(checkin_bp, url_prefix="/checkin")

    @app.route("/")
    def home():
        return {
            "message": "Airline Ticketing API is running"
        }, 200

    return app