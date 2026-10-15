import pytest
import os
from src.pipeline.predict_pipeline import CustomData, PredictPipeline

def test_custom_data_to_dataframe():
    data = CustomData(
        attendance_percentage=90.0,
        eng_math_3=85.0,
        data_structures=88.0,
        digital_logic=82.0,
        oop_java=89.0,
        discrete_math=84.0,
        dbms=86.0,
        operating_systems=85.0,
        computer_networks=88.0,
        design_analysis_algo=90.0,
        software_engineering=92.0
    )
    df = data.get_data_as_data_frame()
    assert df.shape == (1, 11)
    assert "data_structures" in df.columns
    assert "eng_math_3" in df.columns
    assert "design_analysis_algo" in df.columns

def test_predict_pipeline():
    assert os.path.exists("artifacts/model.pkl"), "model.pkl not found"
    assert os.path.exists("artifacts/preprocessor.pkl"), "preprocessor.pkl not found"

    data = CustomData(
        attendance_percentage=85.0,
        eng_math_3=75.0,
        data_structures=78.0,
        digital_logic=72.0,
        oop_java=80.0,
        discrete_math=74.0,
        dbms=77.0,
        operating_systems=75.0,
        computer_networks=76.0,
        design_analysis_algo=79.0,
        software_engineering=82.0
    )
    df = data.get_data_as_data_frame()
    pipeline = PredictPipeline()
    preds = pipeline.predict(df)
    assert len(preds) == 1
    assert 0 <= preds[0] <= 100
