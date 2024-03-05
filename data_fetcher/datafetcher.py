import pandas as pd
from my_utils.linkedlist import LinkedList

class DataFetcher:
    def __init__(self, csv_file, starting_point, ending_point) -> None:
        self.csv_file = csv_file
        self.base_link = "https://resi.stgz.view.com.au/viewstatic/images/listing/acw/800-w/"
        self.starting_point = starting_point
        self.ending_point = ending_point

    def _create_image_link(self, raw_link):
        raw_link_components = raw_link.split("/")
        return self.base_link + raw_link_components[2]

    def fetch_data(self):
        # header = 0: stating that the first row is my header
        # Then, skipping rows from the 1st index to the starting point (not inc starting pt)
        # Finally after that selecting the range of the rows with nrows
        df = pd.read_csv(
            self.csv_file, 
            header=0, 
            skiprows=range(1, self.starting_point), 
            nrows=(self.ending_point - self.starting_point + 1)
        )

        images_info_ll = LinkedList()
        
        for index, row in df.iterrows():
            row_dict = row.to_dict()
            edited_link = self._create_image_link(row_dict["imageLink"])
            row_dict["imageLink"] = edited_link
            images_info_ll.insert_at_end(row_dict)
            # yield row_dict
        
        return images_info_ll