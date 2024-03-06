from data_generator.datafetcher import DataFetcher
from data_generator.objectanalyzer import ObjectAnalyzer
from data_generator.imagedownloader import ImageDownloader
from data_generator.imagefilterer import ImageFilterer

import time

def main():
    start_time = time.time()
    fetcher = DataFetcher("./data/raw/listings_images.csv", starting_point=21, ending_point=30)
    downloader = ImageDownloader()
    analyzer = ObjectAnalyzer()
    filterer = ImageFilterer("./data/interim/batch_2")

    images_information = fetcher.fetch_data()

    images_cache = []
    save_interval = 10
    sleep_interval = 10
    prev_img_number = 20
    image_count = prev_img_number
    index = 0

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

                    image_information["imageNumber"] = index + 1
                    images_cache.append(image_information)

                else:
                    print("Alpha channel containing image found! Discarding it...")
                    images_information.pop(index)
                    continue

            except Exception as e:
                print("An error occured:", e)
                images_information.pop(index)
                continue

            # Saving images info cache to json
            if len(images_cache) == save_interval:
                downloader.save_info_json(images_cache)
                images_cache = []

            if image_count % sleep_interval == 0:
                print("Sleeping...")
                time.sleep(5)
                
            index += 1

        # Saving the remainder of the cache into json
        if len(images_cache) > 0:
            downloader.save_info_json(images_cache)
            images_cache = []

        end_time = time.time()
        print(f"Total time elapsed: {(end_time - start_time) / 60} mins")

    except KeyboardInterrupt as e:
        print("Killing downloader and saving last cache!")
        if len(images_cache) > 0:
            downloader.save_info_json(images_cache)
            images_cache = []

if __name__ == "__main__":
    main()