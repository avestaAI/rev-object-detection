import torch
import logging

class DataGenerator:

    def __init__(self) -> None:
        try:
            model = torch.hub.load('yolov5','custom', path="./yolov5/runs/train/exp5/weights/best.pt",source="local")
        except Exception as e:
            print(e)

    def download_images():
        pass

    def filter_images():
        pass

    def infer(self,):
        pass
