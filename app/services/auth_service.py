from app.models.user import User
from app.extensions import db
from flask_jwt_extended import create_access_token


def register_user(email, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "User already exists"

    user = User(email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user, None


def login_user(email, password):
    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return None, "Invalid credentials"

    token = create_access_token(identity=str(user.id))

    return {
        "access_token": token,
        "user": user.to_dict()
    }, None