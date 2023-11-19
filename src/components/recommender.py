import os
import sys
from dataclasses import dataclass
import pandas as pd
from src.exception import CustomException
from src.logger import logging
from src.utils import save_object_to_file
from sklearn.metrics.pairwise import cosine_similarity
import pdb


@dataclass
class RecommenderTrainingConfig:
    popularity_filepath = os.path.join("artifacts", "popularity.pkl")
    books_filepath = os.path.join("artifacts", "books.pkl")
    collaborative_recommender_filepath = os.path.join("artifacts", "collaborative_recommender.pkl")
    similarity_scores_filepath = os.path.join("artifacts", "similarity_scores.pkl")

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
            popularity_recommender = popularity_recommender.drop_duplicates(subset='Book-Title')

            logging.info("Succesfully built popularity recommender")
            logging.info("Start Building Collaborative filtering recommender")
            user_ratings_count = rating_book_name['User-ID'].value_counts()
            user_ids = user_ratings_count[user_ratings_count > 200].index.tolist()
            filtered_rating = rating_book_name[rating_book_name['User-ID'].isin(user_ids)]
            book_ratings_count = filtered_rating['Book-Title'].value_counts()
            selected_books = book_ratings_count[book_ratings_count >= 50].index.tolist()
            final_filtered_ratings = filtered_rating[filtered_rating['Book-Title'].isin(selected_books)]
            collaborative_filter = final_filtered_ratings.pivot_table(index='Book-Title',columns='User-ID',values='Book-Rating')
            collaborative_filter.fillna(0,inplace=True)
            similarity_scores = cosine_similarity(collaborative_filter)

            logging.info("Succesfully built the Collaborative recommender ")
            
            save_object_to_file(
                file_path=self.training_config.books_filepath,
                obj=books
            )
            
            save_object_to_file(
                file_path=self.training_config.similarity_scores_filepath,
                obj=similarity_scores
            )

            save_object_to_file(
                file_path=self.training_config.collaborative_recommender_filepath,
                obj=collaborative_filter
            )


            save_object_to_file(
                file_path=self.training_config.popularity_filepath,
                obj=popularity_recommender
            )
            logging.info("Saved pickle files")

            return 0
        
        except Exception as e:
            raise CustomException(e,sys)