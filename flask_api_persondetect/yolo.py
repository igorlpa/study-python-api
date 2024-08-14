import math
import cv2
import os
import numpy as np

from typing import List, Optional, Tuple, Union
import torch
import torchvision.transforms as transforms
from ultralytics import YOLO
from ultralytics.engine.results import Results


class Yolo:


    def __init__(self, model_dir=None, device:str = 'cpu'):
        """
        Construtor
        @param model_dir: (string) caminho do diretorio onde o arquivo do modelo a ser usado está
        @param device: definição explicita do device desejado para a detecção ('gpu' ou 'cpu' ou 'mps')
        """

        # Arquivos necessarios para YOLO
        self._model_path = "yolov10l.pt"
        self._model_dir = model_dir
        
        #  usado para indicar caso esteja em outro diretorio
        if model_dir is not None:
            self._model_path = model_dir + '/' + self._model_path
        print('-- '+self._model_path, self._model_dir)
        
        
        if device in ["gpu", "cuda"] and torch.cuda.is_available():
            self.device = torch.device("cuda")
        elif device == 'mps'and torch.backends.mps.is_available():
            self.device = torch.device("mps")
        else:
            self.device = torch.device("cpu")
        
        # Carrega o modelo da YOLO
        self.detector = YOLO(self._model_path, task="detection")

    
    def _detect(self, image_rgb: np.ndarray, threshold = 0.5, classes_to_detect:list = [0]) -> List:
        h, w = image_rgb.shape[:2]

        results = self.detector.predict(
            image_rgb, classes=classes_to_detect, device=self.device, imgsz=640, rect=True
        )[0]  # Pegue o primeiro item da lista, que é o objeto Results

        detections = []

        for det, cls, conf in zip(results.boxes.xyxy, results.boxes.cls, results.boxes.conf):
            if conf >= threshold:
                # Move o tensor para a CPU e o converte para um array numpy, depois para inteiros.
                det = det.cpu().numpy().astype(int)

                # Converte de formato xyxy para xywh
                x0, y0, x1, y1 = det[:4]
                w_box = x1 - x0
                h_box = y1 - y0

                detections.append((int(cls), x0, y0, w_box, h_box, float(conf)))
        return detections
    

    def detect_person(self, image_rgb: np.ndarray):
        """Detector de pessoas em imagens

        Args:
            image_rgb (np.ndarray): imagem no formato RGB

        Returns:
            list: lista de detecções no formato [(cls, x0. y0, h, w, conf)]
        """        
        return self._detect(image_rgb, classes_to_detect=[0])



