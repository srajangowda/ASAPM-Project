import pytest
import os
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

def test_custom_data_to_dataframe():
    data = CustomData(
        gender="female",
        race_ethnicity="group B",
        parental_level_of_education="bachelor's degree",
        lunch="standard",
        test_preparation_course="none",
        reading_score=70.0,
        writing_score=80.0
    )
    df = data.get_data_as_data_frame()
    assert df.shape == (1, 7)
    assert "reading_score" in df.columns
    assert "writing_score" in df.columns

def test_predict_pipeline():
    # Verify artifacts exist before predicting
    assert os.path.exists("artifacts/model.pkl"), "model.pkl not found"
    assert os.path.exists("artifacts/preprocessor.pkl"), "preprocessor.pkl not found"

    data = CustomData(
        gender="female",
        race_ethnicity="group B",
        parental_level_of_education="bachelor's degree",
        lunch="standard",
        test_preparation_course="none",
        reading_score=72.0,
        writing_score=74.0
    )
    df = data.get_data_as_data_frame()
    pipeline = PredictPipeline()
    preds = pipeline.predict(df)
    assert len(preds) == 1
    assert 0 <= preds[0] <= 100

