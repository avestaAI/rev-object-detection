from datagenerator.datagenerator import DataGenerator


def main():
    start = 31
    end = 50
    save_interval = 8
    generator = DataGenerator()
    df = generator.load_csv("./data/raw/listings_images.csv")
    data_dict = generator.load_raw_data(df, start, end)
    generator.download_and_infer(data_dict, start, end, save_interval)
    

if __name__ == "__main__":
    main()
    
