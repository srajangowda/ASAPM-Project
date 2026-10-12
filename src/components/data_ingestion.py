import os
import sys
import pandas as pd
from src.exception import CustomException
from src.logger import logging

from sklearn.model_selection import train_test_split
from dataclasses import dataclass


# Config Class (holds file paths for where data will be stored)
@dataclass   # automatically gives this class an __init__ method
class DataIngestionConfig:
    train_data_path: str = os.path.join("artifacts", "train.csv")
    test_data_path: str = os.path.join("artifacts", "test.csv")
    raw_data_path: str = os.path.join("artifacts", "raw.csv")

# DataIngestion Class (loads the config with those file paths)
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    # Ingestion Method
    def initiate_data_ingestion(self):
        logging.info("Enter the Data Ingestion method or component")
        try:
            df = pd.read_csv(os.path.join("notebook", "data", "stud.csv"))
            logging.info("Read the Dataset as DataFrame")

            # Saving Raw Data
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True)
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info(" i have saved the raw dataset in artifact folder")
        
            # Train-Test Split
            logging.info("Train Test Split Initiated")
            train_set,test_set = train_test_split(df, test_size=0.25, random_state=42)
            logging.info("train test split completed")
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info("Ingestion of the data is completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        
        # Exception Handling
        except Exception as e:
            raise Exception(e, sys)

# Running the Script       
if __name__=="__main__":
    obj= DataIngestion()
    obj.initiate_data_ingestion()
    logging.info("Data ingestion completed successfully!")

# Commands
# python -m src.components.data_ingestion