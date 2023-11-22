import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
import pdb
import numpy as np

class PredictPipeline:
    def __init__(self):
        pass

    def predict_popular(self):
        try:
            popular_df_path = os.path.join("artifacts", "popularity.pkl")
            popular_df=load_object(file_path=popular_df_path)
            book_name = popular_df["Book-Title"].values.tolist()
            author = popular_df["Book-Author"].values.tolist()
            image = popular_df["Image-URL-M"].values.tolist()
            votes = popular_df["num_of_ratings"].values.tolist()
            rating = popular_df["avg_rating"].values.tolist()
            year_publish = popular_df["Year-Of-Publication"].values.tolist()

            return book_name, author, image, votes, rating,year_publish
        
        except Exception as e:
            raise CustomException(e,sys)        
    
    def predict_collaborative(self, book_name):
        try:
            books_path = os.path.join("artifacts", "books.pkl")
            similarity_scores_path =os.path.join("artifacts", "similarity_scores.pkl")
            collaborative_recommender_path = os.path.join("artifacts", "collaborative_recommender.pkl")

            books=load_object(file_path=books_path)
            similarity_scores=load_object(file_path=similarity_scores_path)
            recommender=load_object(file_path=collaborative_recommender_path)

            index = np.where(recommender.index==book_name)[0][0]
            similar_items = sorted(enumerate(similarity_scores[index]), key=lambda x: x[1], reverse=True)[1:11]
            recommended_books  = []
            for i in similar_items:
                item = []
                temp_df = books[books['Book-Title'] == recommender.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Year-Of-Publication'].values))
                item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
                recommended_books.append(item)
            return recommended_books

        except Exception as e:
            raise CustomException(e,sys)