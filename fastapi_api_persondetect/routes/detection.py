import cv2

from schema.schemas import ImageIn, Detection
from src.authentication import login_required
from src.utils import base64_to_opencv_image
from src.yolo import Yolo
from fastapi import status

from fastapi import APIRouter, Depends

router = APIRouter(prefix='/detect')

@router.post('/person', status_code=status.HTTP_200_OK, response_model=list[Detection], dependencies=[Depends(login_required)])
def person_detection(image_in:ImageIn) -> list[Detection]:
    image_rgb = base64_to_opencv_image(image_in.image_base64)
    image_rgb = cv2.cvtColor(image_rgb, cv2.COLOR_BGR2RGB)

    yolo_detector = Yolo(device='mps')
    person_detections = yolo_detector.detect_person(image_rgb)
    print('persons: ', person_detections)
    
    result_detections = []
    for detection in person_detections:
        det = Detection(detection_class=detection[0], 
                        x = detection[1], 
                        y = detection[2],
                        width= detection[3],
                        height= detection[4])
            
        
        result_detections.append(det)
    print('result ',result_detections)
    return result_detections



@router.get("/help")
def help():
    return "HELP - detect"


@router.get("/help-token", dependencies=[Depends(login_required)])
def help_token():
    return "HELP - detect authenticated"