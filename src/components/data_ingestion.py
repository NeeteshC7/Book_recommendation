import os
import sys
from src.exception import CustomException
from src.logger import logging
import pandas as pd

from dataclasses import dataclass
import pdb
from src.utils import save_object_to_file
from src.components.recommender import RecommenderTrainingConfig, RecommenderTrainer

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
            # These are incorrectly placed in Year of Publishing Column
            mask = (books['Year-Of-Publication'] == 'DK Publishing Inc') | (books['Year-Of-Publication'] == 'Gallimard')
            books = books[~mask]

            titles_to_replace = ["The Hitchhiker's Guide to the Galaxy", 'Outlander', 'The Color Purple']
            new_image_url = 'http://images.amazon.com/images/P/0345339711.01.MZZZZZZZ.jpg'
            books.loc[books['Book-Title'].isin(titles_to_replace), 'Image-URL-M'] = new_image_url

           # These URLs aren't same size as other images
            # new_urls = {
            #     'The Hitchhiker\'s Guide to the Galaxy': 'https://m.media-amazon.com/images/I/51MzUz8rQcL._SY445_SX342_.jpg',
            #     'Outlander': 'https://m.media-amazon.com/images/I/41YawkyLcwL._SY445_SX342_.jpg',
            #     'The Color Purple': 'https://m.media-amazon.com/images/I/61y-b4SUdCL._SY445_SX342_.jpg'
            # }
            # books.loc[books['Book-Title'].isin(new_urls.keys()), 'Image-URL-M'] = books['Book-Title'].map(new_urls)



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
    book_path, ratings_path, user_path = obj.initiate_data_ingestion()
    print("Data paths:", book_path, ratings_path, user_path)

    recommender_trainer = RecommenderTrainer()  
    recommender_trainer.initiate_recommender_trainer(book_path, ratings_path, user_path)
