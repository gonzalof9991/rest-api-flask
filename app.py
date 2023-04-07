import os
from flask import Flask, request, jsonify
from flask_smorest import Api
import secrets
# JWT
from flask_jwt_extended import JWTManager
# Importamos los recursos
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint
# Importamos Flask Migrate
from flask_migrate import Migrate
# Importamos la bd
from db import db
# Importamos los modelos
import models
# Importamos BlockList
from blocklist import BLOCKLIST

app = Flask(__name__)
# Configuración de Flask
app.config["API_TITLE"] = "Stores REST API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config["OPENAPI_URL_PREFIX"] = "/"
app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# Configuración DB
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config['SECRET_KEY'] = 'secret!'
db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

# Se utiliza para asegurar que el usuario no ha creado su propio JWT en otro lugar
app.config["JWT_SECRET_KEY"] = "283981440370335659823569030008952160255"
jwt = JWTManager(app)

"""
Cada vez que recibimos un JWT, esta función se ejecuta y comprueba si el token está en la lista de bloqueados,
si esta función devuelve true, entonces la solicitud se termina y el usuario obtendrá un error que dice
el token ha sido revocado o ya no está dispoinble
"""


@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    return jwt_payload["jti"] in BLOCKLIST


# Claims and Authorization
@jwt.additional_claims_loader
def add_claims_to_jwt(identity):
    if identity == 1:
        return {"is_admin": True}
    return {"is_admin": False}


# Configuración de mensajes y errores JWT
@jwt.needs_fresh_token_loader
def token_not_fresh_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {
                "description": "The token is not fresh.",
                "error": "fresh_token_required",
            }
        ),
        401,
    )


@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return (
        jsonify(
            {"description": "The token has been revoked.", "error": "token_revoked"}
        ),
        401,
    )


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return (
        jsonify({"message": "The token has expired.", "error": "token_expired"}),
        401,
    )


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return (
        jsonify(
            {"message": "Signature verification failed.", "error": "invalid_token"}
        ),
        401,
    )


@jwt.unauthorized_loader
def missing_token_callback(error):
    return (
        jsonify(
            {
                "description": "Request does not contain an access token.",
                "error": "authorization_required",
            }
        ),
        401,
    )


# Crear todas las tablas de la bd antes de la consulta
@app.before_first_request
def create_tables():
    print("Creado")
    db.create_all()


# Registramos las rutas
api.register_blueprint(ItemBlueprint)
api.register_blueprint(StoreBlueprint)
api.register_blueprint(TagBlueprint)
api.register_blueprint(UserBlueprint)

if __name__ == '__main__':
    app.run()

"""
1.- Activar virtualenv
2.- .\.venv\Scripts\Activate.ps1
3.- flask run   q
"""
