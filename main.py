from sensor.configuration.mongo_db_conn import mongoDBclient
from sensor.exception import SensorException
import sys,os
from sensor.logger import logging
# from sensor.entity.config_entity import TrainingPipelineConfig,DataIngestionConfig
from sensor.pipeline.training_pipeline import TrainingPipeline

# def test_exception():
#     try:
#         100/0
#     except Exception as e:
#         raise SensorException(e,sys)
    

if __name__ == "__main__":
    # print("hello")
    # mongo_client = mongoDBclient()
    # print(mongo_client.client.test)
    # print(mongo_client.database.list_collection_names())
    # try:
    #     logging.info("Executing test_exception function")
    #     test_exception()
    #     logging.info("test_exception function executed successfully")
    # except Exception as e:
    #     logging.info(e)
    #     print(e)

    # training_pipeline_config = TrainingPipelineConfig()
    # data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
    # print(data_ingestion_config.__dict__)

    training_pipeline = TrainingPipeline()
    training_pipeline.run_pipeline()