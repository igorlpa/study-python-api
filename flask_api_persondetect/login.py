
from http import HTTPStatus
from flask import Blueprint, request
from .authentication import Authentication
from flask_jwt_extended import create_access_token

app = Blueprint("login", __name__, url_prefix="/login")


@app.route("/", methods=["POST"])
def login():
    data = request.json
    secret_key = data.get("secret_key", None)
    if secret_key is None:
        return {"error": "Missing secret key"}, HTTPStatus.BAD_REQUEST
    
    is_authenticated = Authentication.authenticate(secret_key=secret_key)

    if is_authenticated:
        access_token = create_access_token(identity=secret_key)
        return {"token": access_token,}, HTTPStatus.OK
    else:
        return {"error": "Invalid secret key"}, HTTPStatus.UNAUTHORIZED

    

@app.route("/help")
def help():
    return "This is a help page for the login endpoint. \n Send the secret key to get the acitve token via JSON in field 'secret-key' "

