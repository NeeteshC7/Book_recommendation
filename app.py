from flask import Flask,request,render_template
import numpy as np
import pandas as pd
from src.pipeline.predict_pipeline import PredictPipeline

application=Flask(__name__)

app=application

## Route for a home page

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/popularbooks' ,methods=[ 'get','post'])
def popular():
    top_predict_pipeline=PredictPipeline()
    book_name, author, image, votes, rating,year_publish = top_predict_pipeline.predict_popular()
    #print(book_name)
    return render_template('popular.html', book_name=book_name, author=author, image=image, votes=votes, rating=rating, year_publish=year_publish)


@app.route('/recommend',methods=['GET','POST'])
def cf_recommend():
    if request.method == 'GET':
        return render_template('recommend.html')
    else:
        userInput = request.form.get('userInput')
        predict_pipeline=PredictPipeline()
        data = predict_pipeline.predict_collaborative(userInput)
        return render_template('recommend.html', data=data)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__=="__main__":
    app.run(host="0.0.0.0", debug=True) 