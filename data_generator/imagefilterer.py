
class ImageFilterer:

    def __init__(self, base_path) -> None:
        self.base_path = base_path

    def filter_image(self, image_information):
        num_predictions = len(image_information["predictions"])
        image_id = image_information["listingImageId"]

        if num_predictions == 0:
            destination_path = f"{self.base_path}/no_predictions"
            image_name = image_id
        elif num_predictions == 1:
            category = image_information['predictions'][0]['name']
            destination_path = f"{self.base_path}/{category}"
            image_name = f"{category}_{image_id}"
        else:
            categories = "_".join([prediction['name'] for prediction in image_information['predictions']])
            image_name = f"{categories}_{image_id}"
            destination_path = f"{self.base_path}/combinations/{categories}"

        return destination_path, image_name