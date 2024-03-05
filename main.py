from data_generator.datagenerator import DataGenerator
from data_fetcher.datafetcher import DataFetcher

def main():
    # Done till 9640
    # start = 9976
    # end = 16490
    # save_interval = 50
    # sleep_interval = 10
    # prev_image_number = 9640
    # generator = DataGenerator()
    # df = generator.load_csv("./data/raw/listings_images.csv")
    # data_dict = generator.load_raw_data(df, start, end)
    # generator.download_and_infer(data_dict, start, end, prev_image_number, save_interval, sleep_interval)
    fetcher = DataFetcher("./data/raw/listings_images.csv", 5, 10)

    for dict in fetcher.fetch_data():
        print(dict)

    

if __name__ == "__main__":
    main()
    
