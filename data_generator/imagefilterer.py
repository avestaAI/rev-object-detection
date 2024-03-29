
class ImageFilterer:

    def __init__(self, base_path) -> None:
        self.base_path = base_path
        # Please check spelling of category !!!!!!!!!
        self.base_categories = ['swimming_pool','dishwasher','fireplace','garage','tennis_court']

    def filter_image(self, image_information):
        image_id = image_information["listingImageId"]
        
        # detected_categories = list(image_information["predictions"].pandas().xyxy[0]['name'])
        filtered_categories = []
        # print(image_information)

        for prediction in image_information["predictions"]:
            if prediction["name"] in self.base_categories:
                filtered_categories.append(prediction["name"])

        num_predictions = len(filtered_categories)

        # if num_predictions == 0:
        #     destination_path = f"{self.base_path}/no_predictions"
            # image_name = image_id
        if num_predictions == 1:
            destination_path = f"{self.base_path}/{filtered_categories[0]}"
            # category = image_information['predictions'][0]['name']
            # destination_path = f"{self.base_path}/{category}"
            # image_name = image_id
        elif num_predictions > 1:
            destination_path = self.base_path + "/combinations/" + "_".join(filtered_categories)
        else:
            destination_path = None

        return destination_path, image_id