from datagenerator.datagenerator import DataGenerator


def main():
    start = 1
    end = 200
    save_interval = 20
    sleep_interval = 10
    
    generator = DataGenerator()
    df = generator.load_csv("./data/raw/listings_images.csv")
    data_dict = generator.load_raw_data(df, start, end)
    generator.download_and_infer(data_dict, start, end, save_interval, sleep_interval)
    

if __name__ == "__main__":
    main()
    
