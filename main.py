from datagenerator.datagenerator import DataGenerator


def main():
    generator = DataGenerator()
    csv_data = generator.load_csv("./data/raw/listings_images.csv")
    print(csv_data.head(10))


if __name__ == "__main__":
    main()