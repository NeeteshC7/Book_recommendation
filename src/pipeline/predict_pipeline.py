import sys
import os
import pandas as pd
from src.exception import CustomException
from src.utils import load_object
import pdb

class PredictPipeline:
    def __init__(self):
        pass

    def predict(self):
        try:
            popular_df_path = os.path.join("artifacts", "popularity.pkl")
            books_path = os.path.join("artifacts", "books.pkl")
            similarity_scores_path =os.path.join("artifacts", "similarity_scores.pkl")
            # Return the desired values
            popular_df=load_object(file_path=popular_df_path)
            books=load_object(file_path=books_path)
            similarity_scores=load_object(file_path=similarity_scores_path)

            #Replace images for images whose links aren't working
            # titles_to_replace = ["The Hitchhiker's Guide to the Galaxy", 'Outlander', 'The Color Purple']

            # # Define the new URL
            # new_image_url = 'http://images.amazon.com/images/P/0345339711.01.MZZZZZZZ.jpg'

            # # Update Image-URL-M column for specified titles
            # popular_df.loc[popular_df['Book-Title'].isin(titles_to_replace), 'Image-URL-M'] = new_image_url


            book_name = popular_df["Book-Title"].values.tolist()
            author = popular_df["Book-Author"].values.tolist()
            image = popular_df["Image-URL-M"].values.tolist()
            votes = popular_df["num_of_ratings"].values.tolist()
            rating = popular_df["avg_rating"].values.tolist()
            year_publish = popular_df["Year-Of-Publication"].values.tolist()

 

            return book_name, author, image, votes, rating,year_publish
        
        except Exception as e:
            raise CustomException(e,sys)