import os
import sys
import pandas as pd
from src.exception import CustomException
from src.utils import load_object


class PredictPipeline:
    def __init__(self):
        pass

    def predict(self, features):
        try:
            model_path = os.path.join("artifacts", "model.pkl")
            preprocessor_path = os.path.join("artifacts", "preprocessor.pkl")
            
            print("Before Loading")  # Debugging
            model = load_object(file_path=model_path)
            preprocessor = load_object(file_path=preprocessor_path)
            print("After Loading")   # Debugging

            data_scaled = preprocessor.transform(features)
            preds = model.predict(data_scaled)
            return preds
        
        except Exception as e:
            raise CustomException(e, sys)


class CustomData:
    def __init__(self,
                 eng_math_3,
                 data_structures,
                 digital_logic,
                 oop_java,
                 discrete_math,
                 dbms,
                 operating_systems,
                 computer_networks,
                 design_analysis_algo,
                 software_engineering,
                 attendance_percentage=85.0):

        self.eng_math_3 = eng_math_3
        self.data_structures = data_structures
        self.digital_logic = digital_logic
        self.oop_java = oop_java
        self.discrete_math = discrete_math
        self.dbms = dbms
        self.operating_systems = operating_systems
        self.computer_networks = computer_networks
        self.design_analysis_algo = design_analysis_algo
        self.software_engineering = software_engineering
        self.attendance_percentage = attendance_percentage

    def get_data_as_data_frame(self):
        try:
            custom_data_input_dict = {
                "attendance_percentage": [float(self.attendance_percentage)],
                "eng_math_3": [float(self.eng_math_3)],
                "data_structures": [float(self.data_structures)],
                "digital_logic": [float(self.digital_logic)],
                "oop_java": [float(self.oop_java)],
                "discrete_math": [float(self.discrete_math)],
                "dbms": [float(self.dbms)],
                "operating_systems": [float(self.operating_systems)],
                "computer_networks": [float(self.computer_networks)],
                "design_analysis_algo": [float(self.design_analysis_algo)],
                "software_engineering": [float(self.software_engineering)],
            }

            return pd.DataFrame(custom_data_input_dict)

        except Exception as e:
            raise CustomException(e, sys)

