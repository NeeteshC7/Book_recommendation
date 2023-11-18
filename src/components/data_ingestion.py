import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from dataclasses import dataclass

@dataclass
class DataIngestionConfig:
    # Default paths for storing data
    books_path: str = os.path.join('artifacts', 'books.csv')
    users_path: str = os.path.join('artifacts', 'users.csv')
    ratings_path: str = os.path.join('artifacts', 'ratings.csv')

class DataIngestion:
    def __init__(self):
        # Initialize with the configuration for data ingestion
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        # Log entry into the data ingestion process
        logging.info("Starting the data ingestion process")

        try:
            # Read the Books.csv file
            books_dtype = {'Year-Of-Publication': str}
            books = pd.read_csv('notebook/data/Books.csv', dtype=books_dtype)

            # Read the Ratings.csv file
            ratings = pd.read_csv("notebook/data/Ratings.csv")

            # Read the Users.csv file
            users = pd.read_csv("notebook/data/Users.csv")

            # Create necessary directories if they don't exist
            os.makedirs(os.path.dirname(self.ingestion_config.books_path), exist_ok=True)

            # Save the csv file to the 
            books.to_csv(self.ingestion_config.books_path, index=False, header=True)
            ratings.to_csv(self.ingestion_config.ratings_path, index=False, header=True)
            users.to_csv(self.ingestion_config.users_path, index=False, header=True)

            # Log that the dataset has been successfully read
            logging.info('Dataset loaded as a Pandas DataFrame')

            # Return the path to the raw data file
            return (
                self.ingestion_config.books_path,
                self.ingestion_config.ratings_path,
                self.ingestion_config.users_path
            )
        except Exception as e:
            # Raise a custom exception with the encountered error and sys information
            raise CustomException(e, sys)

if __name__=="__main__":
    obj=DataIngestion()
    book_data, ratings_data, user_data = obj.initiate_data_ingestion()
    print("Data paths:", book_data, ratings_data, user_data)
