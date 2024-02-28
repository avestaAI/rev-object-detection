import torch
import pandas as pd
import requests as req
import io
from PIL import Image
import torch
import os
import json
import time
class DataGenerator:

    def __init__(self) -> None:
        self.model = torch.hub.load('./models/yolov5','custom', path="./models/yolov5/runs/train/exp/weights/best.pt", source="local")


    @staticmethod
    def load_csv(csv_path):
        data_df = pd.read_csv(csv_path)
        return data_df
    

    @staticmethod
    def create_link(link):
        base_link = "https://resi.stgz.view.com.au/viewstatic/images/listing/acw/800-w/"
        edited_link = link.split("/")
        return base_link + edited_link[2]
    

    @staticmethod
    def load_raw_data(df, start, end):
        data_dict = []

        for index, row in df.iterrows():
            row_dict = row.to_dict()
            edited_link = DataGenerator.create_link(row_dict["imageLink"])
            row_dict["imageLink"] = edited_link
            data_dict.append(row_dict)

        return data_dict[start-1:end]
    

    @staticmethod
    def download_image(image_link):
        try:
            image_content = req.get(image_link, timeout = 10).content
            image_file = io.BytesIO(image_content)
            pil_image = Image.open(image_file)
            print("-------------------------------------------------------------------------------------------------------")
            print(f"Downloaded: {image_link}")
        except Exception as e:
            print("An error occurred while downloading the image!", e)

        return pil_image
    

    def infer(self, image):
        results = self.model(image)
        return eval(results.pandas().xyxy[0].to_json(orient='records'))
    
    @staticmethod
    def save_image(image, image_path, image_name):
        if not os.path.exists(image_path):
            os.mkdir(image_path)

        with open(f"{image_path}/{image_name}.jpg", "wb") as f:
            image.save(f)
            print(f"Saved: {image_name}.jpg")


    def save_and_filter_image(image, image_info):
        try:
            base_path = './data/interim'

            all_images_path = f"{base_path}/all"
            DataGenerator.save_image(image=image, image_path=all_images_path, image_name = image_info["listingImageId"])

            if len(image_info['predictions']) == 0:
                return 
        
            elif len(image_info['predictions']) == 1:
                category = image_info['predictions'][0]['name']
                full_path = f"{base_path}/{category}"
                image_name = f"{category}_{image_info['listingImageId']}"
                DataGenerator.save_image(image=image, image_path=full_path, image_name=image_name)

            else:
                category = "_".join([prediction['name'] for prediction in image_info['predictions']])
                full_path = f"{base_path}/mix"
                image_name = f"{category}_{image_info['listingImageId']}"
                DataGenerator.save_image(image=image, image_path=full_path, image_name=image_name)
                    
        except Exception as e:
            print(f"Error while saving the image : {e}")

    @staticmethod
    def save_to_json(data_dict):
        try:

            if not os.path.exists("./data/interim/info"):
                os.mkdir("./data/interim/info")

            file_full_path = "./data/interim/info/images_info.json"

            if not os.path.exists(file_full_path):
                with open(file_full_path, "w") as outfile: 
                    outfile.write(json.dumps(data_dict, indent=2))
                    print("\n\nRecords saved to JSON!!")
            else:
                with open(file_full_path, "r") as fp:
                    existing_data_dict = json.load(fp)
                    existing_data_dict.extend(data_dict)

                with open(file_full_path, "w") as outfile: 
                    outfile.write(json.dumps(existing_data_dict, indent=2))
                    print("\n\nRecords saved to JSON!!")
        except Exception as e:
            print("Error saving json file!", e)


    def download_and_infer(self, data_dict, start, end, save_interval):
        try:
            index = 0
            start_time = time.time()
            while index < len(data_dict):
                image_link = data_dict[index]['imageLink']
                image = DataGenerator.download_image(image_link)

                if len(image.getbands()) <= 3:
                    results = self.infer(image)
                    data_dict[index]['predictions'] = results
                    data_dict[index]['imageNumber'] = start + index
                    print("Image Number:", start + index)

                    DataGenerator.save_and_filter_image(image, data_dict[index])
                
                else:
                    print("An image with alpha channel found, hence discarding it!")
                    data_dict.pop(index)
                    continue
                
                if (index + 1) % save_interval == 0:
                    DataGenerator.save_to_json(data_dict[index+1-save_interval:index+1])
                    print("Sleeping...\n\n")
                    time.sleep(4)

                index += 1

            remainder = index % save_interval

            if remainder > 0:
                DataGenerator.save_to_json(data_dict[-remainder:])

            end_time = time.time()
            print(f"Total time elapsed: {(end_time - start_time) / 60} mins")
        except KeyboardInterrupt:
            DataGenerator.save_to_json(data_dict[index - save_interval:index])
        # print(data_dict)