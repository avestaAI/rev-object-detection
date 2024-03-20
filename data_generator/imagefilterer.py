
class ImageFilterer:

    def __init__(self, base_path) -> None:
        self.base_path = base_path
        # Please check spelling of category !!!!!!!!!
        self.base_categories = ['swimming_pool','dishwasher','fireplace','garage','tennis_court']  

    def filter_image(self, image_information):
        num_predictions = len(image_information["predictions"])
        image_id = image_information["listingImageId"]

        if num_predictions == 0:
            destination_path = f"{self.base_path}/no_predictions"
            image_name = image_id
        elif num_predictions == 1:
            category = image_information['predictions'][0]['name']
            destination_path = f"{self.base_path}/{category}"
            image_name = image_id
        else:
            flag = 0
            prediction_categories = [prediction['name'] for prediction in image_information['predictions']]
            for i in self.base_categories:
                if i in prediction_categories:
                    flag = 1
            
            # categories = "_".join([prediction['name'] for prediction in image_information['predictions']])
            image_name = image_id
            if flag:
                destination_path = f"{self.base_path}/combinations"
            else:
                destination_path = f"{self.base_path}/other_combinations"

        return destination_path, image_name