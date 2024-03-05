from data_fetcher.datafetcher import DataFetcher
from object_analyzer.objectanalyzer import ObjectAnalyzer
from image_downloader.imagedownloader import ImageDownloader
from image_filterer.imagefilterer import ImageFilterer

import time


def main():
    start_time = time.time()
    fetcher = DataFetcher("./data/raw/listings_images.csv", starting_point=21, ending_point=30)
    downloader = ImageDownloader()
    analyzer = ObjectAnalyzer()
    filterer = ImageFilterer("./data/interim/batch_2")

    images_info_linked_list = fetcher.fetch_data()

    ptr = images_info_linked_list.head
    images_cache = []
    save_interval = 10
    sleep_interval = 10
    prev_img_number = 20
    image_count = prev_img_number

    try:
        while(ptr != None):
            try:
                image_link = ptr.data["imageLink"]
                image_data = downloader.get_image_data(image_link)

                # Checking whether the images contains alpha channel or not
                if len(image_data.getbands()) <= 3:
                    results = analyzer.analyze_objects(image_data)
                    ptr.data["predictions"] = results

                    destination_path, image_name = filterer.filter_image(ptr.data)
                    downloader.save_image(image_data, destination_path, image_name)

                    image_count += 1
                    ptr.data["imageNumber"] = image_count
                    images_cache.append(ptr.data)

                else:
                    print("Alpha channel containing image found! Discarding it...")
                    images_info_linked_list.remove(ptr.data)

            except Exception as e:
                print("An error occured : ",e)
                images_info_linked_list.remove(ptr.data)

            if len(images_cache) == save_interval:
                downloader.save_info_json(images_cache)
                images_cache = []

            if image_count % sleep_interval == 0:
                print("Sleeping...")
                time.sleep(5)
                
            ptr = ptr.next

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