from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.docs.swagger import swagger_template

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
swagger = Swagger(template=swagger_template)
limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://"
)