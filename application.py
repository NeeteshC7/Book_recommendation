from flask import Flask,request,render_template
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline

application=Flask(__name__)

application=application

## Route for a home page

@application.route('/')
def index():
    return render_template('index.html') 

@application.route('/popularbooks' ,methods=[ 'get','post'])
def popular():
    top_predict_pipeline=PredictPipeline()
    book_name, author, image, votes, rating,year_publish = top_predict_pipeline.predict_popular()
    #print(book_name)
    return render_template('popular.html', book_name=book_name, author=author, image=image, votes=votes, rating=rating, year_publish=year_publish)


@application.route('/recommend',methods=['GET','POST'])
def cf_recommend():
    if request.method == 'GET':
        return render_template('recommend.html')
    else:
        userInput = request.form.get('userInput')
        predict_pipeline=PredictPipeline()
        data = predict_pipeline.predict_collaborative(userInput)
        return render_template('recommend.html', data=data)

@application.route('/contact')
def contact():
    return render_template('contact.html')

if __name__=="__main__":
    application.run(host="0.0.0.0") 