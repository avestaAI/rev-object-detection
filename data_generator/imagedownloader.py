import requests as req
import io
from PIL import Image
import os
import json


class ImageDownloader:

    def __init__(self, base_path) -> None:
        self.base_path = base_path

    @staticmethod
    def get_image_data(image_link):
        image_content = req.get(image_link, timeout = 10).content
        image_file = io.BytesIO(image_content)
        pil_image = Image.open(image_file)
        print("-------------------------------------------------------------------------------------------------------")
        print(f"Downloaded: {image_link}")
        return pil_image

    @staticmethod
    def save_image(image_data, destination_path, image_name):
        if not os.path.exists(destination_path):
            # Note here os.makedirs
            # makes directories recursively if not available
            os.makedirs(destination_path, exist_ok=True)

        with open(f"{destination_path}/{image_name}.jpg", "wb") as f:
            image_data.save(f)
            print(f"Saved: {image_name}.jpg")

    
    def save_info_json(self, images_info):

        if not os.path.exists(f"{self.base_path}/info"):
            os.mkdir(f"{self.base_path}/info")

        destination_path = f"{self.base_path}/info/images_info.json"

        if not os.path.exists(destination_path):
            with open(destination_path, "w") as outfile: 
                outfile.write(json.dumps(images_info, indent=2))
                print("\n\nRecords saved to JSON!!\n\n")
        else:
            with open(destination_path, "r") as fp:
                existing_data_dict = json.load(fp)
                existing_data_dict.extend(images_info)

            with open(destination_path, "w") as outfile: 
                outfile.write(json.dumps(existing_data_dict, indent=2))
                print("\n\nRecords saved to JSON!!\n\n")