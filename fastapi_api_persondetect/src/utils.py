import base64
import numpy as np
import cv2


def base64_to_opencv_image(base64_string):
    """
    Converte uma string base64 para uma imagem OpenCV.

    Args:
        base64_string (str): A string base64 representando a imagem.

    Returns:
        numpy.ndarray: A matriz NumPy representando a imagem OpenCV.
    """

    # Decodifica a string base64
    img_data = base64.b64decode(base64_string)

    # Cria um NumPy array a partir dos bytes decodificados
    np_arr = np.frombuffer(img_data, np.uint8)

    # Decodifica o NumPy array para uma imagem OpenCV
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    return img
