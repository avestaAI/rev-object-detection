import torch
import pandas as pd
class DataGenerator:

    def __init__(self) -> None:
        self.model = torch.hub.load('./models/yolov5','custom', path="./models/yolov5/runs/train/exp/weights/best.pt", source="local")
        self.images_info = []

    @staticmethod
    def load_csv(self, csv_path):
        data_df = pd.read_csv(csv_path)
        return data_df
    
    @staticmethod
    def create_link():
        pass

    
        

    
    

    # def download_image(self, image_link):
    #     self.image_info = {}
        
    #     #download image from link

    #     # return img # Image RGB arr
        

    # def filter_images():
    #     pass

    # def infer(self,img):
    #     try:
    #         result = self.model(img)
    #         self.image_info['infer'] = eval(result.pandas().xyxy[0].to_json(orient='records'))
    #     except Exception as e:
    #         print(f"Error at infering image : {self.image_info['name']}")
    

        



