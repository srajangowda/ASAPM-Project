from flask import Flask, request, render_template
import numpy as np
import pandas as pd

from src.pipeline.predict_pipeline import CustomData, PredictPipeline

app = Flask(__name__)

# Home page
@app.route('/')
def index():
    return render_template('index.html')

# Form page
@app.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        data = CustomData(
            gender=request.form.get('gender'),
            race_ethnicity=request.form.get('ethnicity'),
            parental_level_of_education=request.form.get('parental_level_of_education'),
            lunch=request.form.get('lunch'),
            test_preparation_course=request.form.get('test_preparation_course'),
            reading_score=float(request.form.get('reading_score')),
            writing_score=float(request.form.get('writing_score'))
        )
        pred_df = data.get_data_as_data_frame()
        predict_pipeline = PredictPipeline()
        results = predict_pipeline.predict(pred_df)
        score = round(float(results[0]), 1)
        student_data = {
            'gender': request.form.get('gender'),
            'ethnicity': request.form.get('ethnicity'),
            'parental_education': request.form.get('parental_level_of_education'),
            'lunch': request.form.get('lunch'),
            'test_prep': request.form.get('test_preparation_course'),
            'reading_score': float(request.form.get('reading_score')),
            'writing_score': float(request.form.get('writing_score'))
        }
        return render_template('result.html', results=score, student=student_data)
    return render_template('form.html')

# Result page
@app.route('/result')
def result():
    return render_template('result.html')

# Home redirect
@app.route('/home')
def home():
    return render_template('index.html')

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
