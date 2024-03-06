import os
import json


class Statistics:

    def __init__(self, base_path) -> None:
        self.stats = {}
        self.base_path = base_path

    def record_stats(self, image_information):
        for prediction in image_information["predictions"]:
            category = prediction["name"] 
            if category in self.stats.keys():
                self.stats[category] += 1
            else:
                self.stats[category] = 1

    def save_stats(self):
        if not os.path.exists(f"{self.base_path}/info"):
            os.mkdir(f"{self.base_path}/info")

        destination_path = f"{self.base_path}/info/stats.json"

        with open(destination_path, "w") as outfile: 
            outfile.write(json.dumps(self.stats, indent=2))
            print("\n\Stats saved to JSON!!\n\n")
