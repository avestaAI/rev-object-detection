from data_generator.datafetcher import DataFetcher
from data_generator.objectanalyzer import ObjectAnalyzer
from data_generator.imagedownloader import ImageDownloader
from data_generator.imagefilterer import ImageFilterer
from data_generator.statistics import Statistics
from PIL import UnidentifiedImageError
from requests.exceptions import ConnectionError

import time

config = {
    "save_interval": 10,
    "sleep_interval": 10,
    "last_img_number": 0
}

def main():
    base_path = "./data/interim/batch_2"
    start_time = time.time()
    fetcher = DataFetcher(
        "./data/raw/listings_images.csv", 
        starting_point=1, 
        ending_point=30
    )
    downloader = ImageDownloader(base_path)
    analyzer = ObjectAnalyzer()
    filterer = ImageFilterer(base_path)
    statistics = Statistics(base_path)

    images_information = fetcher.fetch_data()

    images_cache = []
    index = 0
    failed_images = 0

    try:
        while(index < len(images_information)):
            try:
                image_information = images_information[index]

                image_link = image_information["imageLink"]
                image_data = downloader.get_image_data(image_link)

                # Checking whether the images contains alpha channel or not
                if len(image_data.getbands()) <= 3:
                    results = analyzer.analyze_objects(image_data)
                    image_information["predictions"] = results

                    destination_path, image_name = filterer.filter_image(image_information)
                    downloader.save_image(image_data, destination_path, image_name)
                    statistics.record_stats(image_information)

                    image_information["imageNumber"] = (index + 1) + config["last_img_number"]
                    images_cache.append(image_information)

                else:
                    print("Alpha channel containing image found! Discarding it...")
                    failed_images += 1
                    images_information.pop(index)
                    continue

            except ConnectionError as e:
                    print("Connection error, retrying after 10 seconds")
                    time.sleep(10)
                    continue
            
            except UnidentifiedImageError as e:
                print("Image not found in the given link!")
                failed_images += 1
                images_information.pop(index)
                continue

            except Exception as e:
                print("Something went wrong!")
                failed_images += 1
                images_information.pop(index)
                continue

            # Saving images info cache to json
            if len(images_cache) == config["save_interval"]:
                downloader.save_info_json(images_cache)
                statistics.save_stats()
                images_cache = []

            if (index + 1) % config["sleep_interval"] == 0:
                print("Sleeping...")
                time.sleep(5)
                
            index += 1

        # Saving the remainder of the cache into json
        if len(images_cache) > 0:
            downloader.save_info_json(images_cache)
            statistics.save_stats()
            images_cache = []

        end_time = time.time()
        print(f"Total time elapsed: {(end_time - start_time) / 60} mins")
        print("Failed images:", failed_images)

    except KeyboardInterrupt as e:
        print("Killing downloader and saving last cache!")
        if len(images_cache) > 0:
            downloader.save_info_json(images_cache)
            statistics.save_stats()
            images_cache = []

if __name__ == "__main__":
    main()