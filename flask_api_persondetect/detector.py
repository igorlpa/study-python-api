
from http import HTTPStatus
import json
from flask import Blueprint, request
from .authentication import Authentication
from flask_jwt_extended import jwt_required
from .utils import base64_to_opencv_image
from .yolo import Yolo

app = Blueprint("detector", __name__, url_prefix="/detect")


@app.route("/person", methods=["POST"])
@jwt_required()
def detect_person():
    data = request.json
    image_base64 = data.get("image_base64", None)

    if image_base64 is None or image_base64 == "":
        return {"error": "No image base64"}, HTTPStatus.BAD_REQUEST
    try:
        image_rgb = base64_to_opencv_image(image_base64)
    except:
        return {"error": "base64 format invalid"}, HTTPStatus.BAD_REQUEST  

    yolo_detector = Yolo(device='mps')
    person_detections = yolo_detector.detect_person(image_rgb)
    json_data = []
    for detection in person_detections:
        data = {
            "class": detection[0],
            "x": int(detection[1]),
            "y": int(detection[2]),
            "width": int(detection[3]),
            "height": int(detection[4])
        }
        json_data.append(data)
    result = {"detections":json_data}
    json_string = json.dumps(result)     
    return json_string, HTTPStatus.OK



@app.route("/help")
def help():
    return "HELP - detect"

@app.route("/help-token")
@jwt_required()
def help_token():
    return "HELP - detect authenticated"