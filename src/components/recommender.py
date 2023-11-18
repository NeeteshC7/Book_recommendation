import os
import sys
from dataclasses import dataclass
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object_to_file
import pdb


@dataclass
class RecommenderTrainingConfig:
    popularity_filepath = os.path.join("artifacts", "popularity.pkl")
   # collaborative_filepath = os.path.join("artifacts", "collaborative.pkl")

class RecommenderTrainer:
    def __init__(self):
        self.training_config = RecommenderTrainingConfig()

    def initiate_recommender_trainer(self, book_path, rating_path, user_path):
        try:
            logging.info("Recommender building start")
            books = pd.read_csv(book_path)
            ratings = pd.read_csv(rating_path)
            users = pd.read_csv(user_path)

            rating_book_name = ratings.merge(books,on='ISBN')
            num_of_rating_df = rating_book_name.groupby('Book-Title').count()['Book-Rating'].reset_index()
            num_of_rating_df.rename(columns={'Book-Rating':'num_of_ratings'},inplace=True)

            avg_rating_df = rating_book_name.groupby('Book-Title').mean(numeric_only=True)['Book-Rating'].reset_index()
            avg_rating_df.rename(columns={'Book-Rating':'avg_rating'},inplace=True)

            popular_df = num_of_rating_df.merge(avg_rating_df,on='Book-Title')
            popularity_recommender = popular_df[popular_df['num_of_ratings']>=250].sort_values('avg_rating',ascending=False).head(50)
            popularity_recommender = popularity_recommender.merge(books,on='Book-Title').drop_duplicates('Book-Title')[['Book-Title','Book-Author','Year-Of-Publication','Image-URL-M','num_of_ratings','avg_rating' ]]

            save_object_to_file(
                file_path=self.training_config.popularity_filepath,
                obj=popularity_recommender
            )
            logging.info("Succesfully built popularity recommender")
            return 0
        
        except Exception as e:
            raise CustomException(e,sys)