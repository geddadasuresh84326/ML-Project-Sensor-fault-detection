from sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from sensor.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from sensor.entity.config_entity import DataValidationConfig
from sensor.utils.main_utils import read_yaml_file,write_yaml_file
from sensor.exception import SensorException
from sensor.logger import logging
import pandas as pd
import numpy as np
import sys,os
from scipy.stats import ks_2samp

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys)
    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            no_of_columns = len(self._schema_config["columns"])
            logging.info(f"number of columns in schema file : {no_of_columns}")
            logging.info(f"number of columns in dataframe  : {len(dataframe.columns)}")

            if len(dataframe.columns) == no_of_columns:
                return True
            return False
        except Exception as e:
            raise SensorException(e,sys)
    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            no_of_columns = len(self._schema_config["numerical_columns"])
            df_columns = dataframe.columns
            numerical_columns_status = True
            missing_numerical_columns = []
            for numerical_col in self._schema_config["numerical_columns"]:
                if numerical_col not in df_columns:
                    numerical_columns_status = False
                    missing_numerical_columns.append(numerical_col)
            logging.info(f"missing numerical columns: [{missing_numerical_columns}]")

            return numerical_columns_status
        
        except Exception as e:
            raise SensorException(e,sys)

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise SensorException(e,sys)

    def detect_dataset_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1,d2)
                if threshold <= is_same_dist.pvalue:
                    is_found = False
                else:
                    status = False
                    is_found = True
                report.update({column:{
                    "pvalue : ":float(is_same_dist.pvalue),
                    "drift_status : ":is_found}
                })
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path

            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(file_path=drift_report_file_path,content=report)

            return status
        except Exception as e:
            raise SensorException(e,sys)

    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_message = ""
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path  = self.data_ingestion_artifact.test_file_path

            # Reading data from the train and test file location
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path)

            #Validate No.of columns
            status = self.validate_number_of_columns(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe doesn't contain all columns\n"
            status = self.validate_number_of_columns(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe doesn't contain all columns\n"

            # Validate numerical columns
            status = self.is_numerical_column_exist(dataframe=train_dataframe)
            if not status:
                error_message = f"{error_message} Train dataframe doesn't contain all numerical columns\n"
            status = self.is_numerical_column_exist(dataframe=test_dataframe)
            if not status:
                error_message = f"{error_message} Test dataframe doesn't contain all numerical columns\n"
            if len(error_message)>0:
                raise Exception(error_message)
            
            # lets check data drift
            self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            
            data_validation_artifact = DataValidationArtifact(
                validation_status= status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path= None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact
        except Exception as e:
            raise SensorException(e,sys)
        