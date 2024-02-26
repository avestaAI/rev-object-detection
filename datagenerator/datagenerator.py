import torch
import logging

class DataGenerator:

    def __init__(self) -> None:
        self.model = torch.hub.load('yolov5','custom', path="./yolov5/runs/train/exp5/weights/best.pt",source="local")
        self.images_info = []

    def download_images(self,image_link):
        #download image from link

        return img # Image RGB arr

    def filter_images():
        pass

    def infer(self,img):
        result = self.model(img)
        self.image_info['class'] = list(result.pandas().xyxy[0]['class'])
        self.image_info['name'] = list(result.pandas().xyxy[0]['name'])
        self.image_info['xyxy'] = list(result.xyxy[0][:,:-2])
        self.image_info['confidence'] = list(result.xyxy[0][:,4])
    
    def load_csv(self, csv_path):
        image_links = None #load csv from csv_path to list
        for link in image_links:
            self.image_info = {}
            img = download_images(link)
            infer(img)
            self.images_info.append(self.image_info)
            filter_images()




