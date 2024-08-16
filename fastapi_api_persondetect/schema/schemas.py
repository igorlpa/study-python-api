
from pydantic import BaseModel

class Detection(BaseModel):
    detection_class:int
    x:int
    y:int
    width:int
    height:int

    # def __init__(self, class_label:int, x:int, y:int, width:int, height:int):
    #     self.detection_class = class_label
    #     self.x = x
    #     self.y = y
    #     self.width = width
    #     self.height = height


class ImageIn(BaseModel):
    image_base64:str

class Login(BaseModel):
    secret_key:str

class LoginOut(BaseModel):
    token:str