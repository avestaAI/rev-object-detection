from datagenerator.datagenerator import DataGenerator


def main():
    generator = DataGenerator()
    csv_data = generator.load_csv("./data/raw/listings_images.csv")
    print(csv_data.head(10))
    data_dict = generator.load_raw_data(csv_data)

    for data in data_dict:




if __name__ == "__main__":
    main()



for index,data in enumerate(data_dict):
    
