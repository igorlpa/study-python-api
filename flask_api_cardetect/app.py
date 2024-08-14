import os 
from http import HTTPStatus

from flask import Flask, json, request
from . import login
from . import detector
from flask_jwt_extended  import JWTManager

jwt = JWTManager()


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    print(__name__)

    app.config.from_mapping(
        SECRET_KEY='dev',
        JWT_SECRET_KEY="super-secret"
    )
    # inicializar componentes necessarios, como BD por exemplo

    #register blueprints
    app.register_blueprint(login.app)
    app.register_blueprint(detector.app)


    # init plugins
    jwt.init_app(app)

    @app.route("/")
    def home():
        return 'Home - Detector de carros API Flask'


    return app  

