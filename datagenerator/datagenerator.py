import torch
import pandas as pd
import requests as req
from requests.exceptions import ConnectionError
import io
from PIL import Image
from PIL import UnidentifiedImageError
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
        image_content = req.get(image_link, timeout = 10).content
        image_file = io.BytesIO(image_content)
        pil_image = Image.open(image_file)
        print("-------------------------------------------------------------------------------------------------------")
        print(f"Downloaded: {image_link}")
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


    @staticmethod
    def save_and_filter_image(image, image_info):
        base_path = './data/interim'

        all_images_path = f"{base_path}/all"
        DataGenerator.save_image(image=image, image_path=all_images_path, image_name = image_info["listingImageId"])

        if len(image_info['predictions']) == 0:
            full_path = f"{base_path}/no_predictions"
            image_name = f"{image_info['listingImageId']}"
            DataGenerator.save_image(image=image,image_path=full_path,image_name=image_name)
    
        elif len(image_info['predictions']) == 1:
            category = image_info['predictions'][0]['name']
            full_path = f"{base_path}/{category}"
            image_name = f"{category}_{image_info['listingImageId']}"
            DataGenerator.save_image(image=image, image_path=full_path, image_name=image_name)

        else:
            if not os.path.exists(f"{base_path}/combinations"):
                os.mkdir(f"{base_path}/combinations")

            category = "_".join([prediction['name'] for prediction in image_info['predictions']])
            image_name = f"{category}_{image_info['listingImageId']}"
            full_path = f"{base_path}/combinations/{category}"
            DataGenerator.save_image(image=image, image_path=full_path, image_name=image_name)
                    

    @staticmethod
    def save_to_json(data_dict):
        if not os.path.exists("./data/interim/info"):
            os.mkdir("./data/interim/info")

        file_full_path = "./data/interim/info/images_info.json"

        if not os.path.exists(file_full_path):
            with open(file_full_path, "w") as outfile: 
                outfile.write(json.dumps(data_dict, indent=2))
                print("\n\nRecords saved to JSON!!\n\n")
        else:
            with open(file_full_path, "r") as fp:
                existing_data_dict = json.load(fp)
                existing_data_dict.extend(data_dict)

            with open(file_full_path, "w") as outfile: 
                outfile.write(json.dumps(existing_data_dict, indent=2))
                print("\n\nRecords saved to JSON!!\n\n")


    def download_and_infer(self, data_dict, start, end, save_interval, sleep_interval):
        try:
            index = 0
            failed_images = 0
            start_time = time.time()
            while index < len(data_dict):

                try:
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

                except ConnectionError as e:
                    print("Connection error, retrying after 10 seconds")
                    time.sleep(10)
                    continue
                except UnidentifiedImageError as e:
                    print("Image not found in the given link!")
                    failed_images += 1
                    data_dict.pop(index)
                    continue
                except Exception as e:
                    print("Something went wrong!")
                    failed_images += 1
                    data_dict.pop(index)
                    continue


                if (index + 1) % save_interval == 0:
                    DataGenerator.save_to_json(data_dict[index+1-save_interval:index+1])

                if (index + 1) % sleep_interval == 0:
                    print("\n\nSleeping...\n\n")
                    time.sleep(4)

                index += 1


            remainder = index % save_interval
            if remainder > 0:
                DataGenerator.save_to_json(data_dict[-remainder:])

            end_time = time.time()
            print(f"Total time elapsed: {(end_time - start_time) / 60} mins")
            print(f"Total images: {end - start + 1} | Succeded Images: {(end - start + 1) - failed_images} | Failed images: {failed_images}")
        except KeyboardInterrupt:
            DataGenerator.save_to_json(data_dict[index - save_interval:index])